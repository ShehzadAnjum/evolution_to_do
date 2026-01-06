/*
 * Evolution Todo - IoT Controller
 * Version: 2.8 (LCD message display with blinking header and RGB cycling)
 */

#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <esp_wifi.h>
#include <time.h>
#include "config.h"

// ============================================
// RGB LED Colors
// ============================================
struct RGB { uint8_t r, g, b; };

const RGB COLOR_OFF     = {0, 0, 0};
const RGB COLOR_RED     = {255, 0, 0};
const RGB COLOR_GREEN   = {0, 255, 0};
const RGB COLOR_BLUE    = {0, 0, 255};
const RGB COLOR_YELLOW  = {255, 200, 0};
const RGB COLOR_MAGENTA = {255, 0, 255};
const RGB COLOR_CYAN    = {0, 255, 255};
const RGB COLOR_ORANGE  = {255, 80, 0};

const uint8_t BRIGHT = 200;
const uint8_t DULL   = 40;

// Screen timing
const unsigned long TIME_SCREEN_DURATION = 15000;
const unsigned long STATUS_SCREEN_DURATION = 3000;

// ============================================
// Global Objects
// ============================================
WiFiClientSecure wifiClient;
PubSubClient mqtt(wifiClient);
LiquidCrystal_I2C lcd(LCD_ADDRESS, 16, 2);

// ============================================
// State
// ============================================
struct SystemState {
  bool lcdReady;
  bool wifiConnected;
  bool timeSync;
  bool mqttConnected;
  bool allReady;
  bool relays[4];
} state = {false, false, false, false, false, {false, false, false, false}};

// ============================================
// Timers
// ============================================
struct Timers {
  unsigned long wifiCheck;
  unsigned long mqttReconnect;
  unsigned long heartbeat;
  unsigned long scheduleCheck;
  unsigned long screenChange;
  unsigned long ntpRetry;
  unsigned long ledBlink;
} timers = {0};

// LED Blink State
bool ledBlinking = false;
bool ledBlinkState = false;
RGB blinkColor = COLOR_OFF;
uint8_t blinkBrightness = DULL;
unsigned long blinkInterval = 300;

// Screen State
uint8_t currentScreen = 0;
bool showingTimeScreen = true;
char lastLine1[17] = "";
char lastLine2[17] = "";
uint8_t lastSecond = 255;

// Message Display State
bool messageMode = false;
char messageText[128] = "";
unsigned long messageStartTime = 0;
unsigned long messageBlinkTime = 0;
unsigned long messageScrollTime = 0;
unsigned long messageColorTime = 0;
bool messageHeaderVisible = true;
int messageScrollPos = 0;
uint8_t messageColorIndex = 0;
const unsigned long MESSAGE_DURATION = 60000;  // 1 minute
const unsigned long MESSAGE_BLINK_INTERVAL = 500;  // Header blink every 500ms
const unsigned long MESSAGE_SCROLL_INTERVAL = 200;  // Scroll speed
const unsigned long MESSAGE_COLOR_INTERVAL = 500;  // Color change every 500ms

// RGB color cycle array
const RGB MESSAGE_COLORS[] = {
  COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_YELLOW,
  COLOR_MAGENTA, COLOR_CYAN, COLOR_ORANGE
};
const uint8_t MESSAGE_COLOR_COUNT = 7;

// ============================================
// Schedule Storage
// ============================================
struct Schedule {
  char id[40];
  uint8_t relay;
  char action[8];
  time_t executeAt;
  bool active;
  bool countdownStarted;
};
Schedule schedules[MAX_SCHEDULES];
uint8_t scheduleCount = 0;

// ============================================
// Constants
// ============================================
const uint8_t RELAY_PINS[4] = {RELAY_1_PIN, RELAY_2_PIN, RELAY_3_PIN, RELAY_4_PIN};
const char* RELAY_NAMES[4] = {RELAY_1_NAME, RELAY_2_NAME, RELAY_3_NAME, RELAY_4_NAME};

// ============================================
// Debug
// ============================================
#if DEBUG_SERIAL
  #define LOG(x) Serial.println(x)
  #define LOGF(...) Serial.printf(__VA_ARGS__)
#else
  #define LOG(x)
  #define LOGF(...)
#endif

// ============================================
// LED Functions
// ============================================
void ledSet(RGB color, uint8_t brightness) {
  uint8_t r = (color.r * brightness) / 255;
  uint8_t g = (color.g * brightness) / 255;
  uint8_t b = (color.b * brightness) / 255;
  neopixelWrite(RGB_PIN, r, g, b);
}

void ledOff() {
  ledBlinking = false;
  neopixelWrite(RGB_PIN, 0, 0, 0);
}

void ledSolid(RGB color, uint8_t brightness) {
  ledBlinking = false;
  ledSet(color, brightness);
}

void ledStartBlink(RGB color, uint8_t brightness, unsigned long interval) {
  ledBlinking = true;
  blinkColor = color;
  blinkBrightness = brightness;
  blinkInterval = interval;
  ledBlinkState = true;
  timers.ledBlink = millis();
  ledSet(color, brightness);
}

void ledUpdate() {
  if (!ledBlinking) return;

  unsigned long now = millis();
  if (now - timers.ledBlink >= blinkInterval) {
    timers.ledBlink = now;
    ledBlinkState = !ledBlinkState;
    if (ledBlinkState) {
      ledSet(blinkColor, blinkBrightness);
    } else {
      neopixelWrite(RGB_PIN, 0, 0, 0);
    }
  }
}

void ledFlash(RGB color, uint8_t brightness, int times, int intervalMs) {
  ledBlinking = false;
  for (int i = 0; i < times; i++) {
    ledSet(color, brightness);
    delay(intervalMs);
    neopixelWrite(RGB_PIN, 0, 0, 0);
    delay(intervalMs);
  }
}

// ============================================
// LCD Functions (No Flicker)
// ============================================
void lcdClear() {
  lcd.clear();
  lastLine1[0] = '\0';
  lastLine2[0] = '\0';
}

void lcdSetLine(int line, const char* text) {
  char padded[17];
  snprintf(padded, 17, "%-16s", text);  // Pad to 16 chars

  if (line == 0) {
    if (strcmp(padded, lastLine1) != 0) {
      lcd.setCursor(0, 0);
      lcd.print(padded);
      strncpy(lastLine1, padded, 16);
      lastLine1[16] = '\0';
    }
  } else {
    if (strcmp(padded, lastLine2) != 0) {
      lcd.setCursor(0, 1);
      lcd.print(padded);
      strncpy(lastLine2, padded, 16);
      lastLine2[16] = '\0';
    }
  }
}

// Scroll long text on specified line (blocking, fast scroll)
void lcdScrollLine(int line, const char* text, int delayMs = 150) {
  int len = strlen(text);
  if (len <= 16) {
    // No need to scroll, just display
    lcdSetLine(line, text);
    delay(1500);
    return;
  }

  // Add padding for smooth scroll
  char scrollBuf[64];
  snprintf(scrollBuf, 64, "%s    ", text);  // Add spaces at end
  int scrollLen = strlen(scrollBuf);

  // Show initial text
  char display[17];
  strncpy(display, scrollBuf, 16);
  display[16] = '\0';
  lcd.setCursor(0, line);
  lcd.print(display);
  delay(800);  // Pause before scrolling

  // Scroll through text
  for (int i = 1; i <= scrollLen - 16; i++) {
    strncpy(display, scrollBuf + i, 16);
    display[16] = '\0';
    lcd.setCursor(0, line);
    lcd.print(display);
    delay(delayMs);
  }

  delay(500);  // Pause at end
}

void lcdShow(const char* line1, const char* line2) {
  lcdSetLine(0, line1);
  if (line2) {
    lcdSetLine(1, line2);
  }
}

void lcdShowForce(const char* line1, const char* line2) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(line1);
  strncpy(lastLine1, line1, 16);
  lastLine1[16] = '\0';

  if (line2) {
    lcd.setCursor(0, 1);
    lcd.print(line2);
    strncpy(lastLine2, line2, 16);
    lastLine2[16] = '\0';
  }
}

// ============================================
// MESSAGE DISPLAY MODE
// ============================================
void startMessageMode(const char* message) {
  messageMode = true;
  strncpy(messageText, message, 127);
  messageText[127] = '\0';
  messageStartTime = millis();
  messageBlinkTime = millis();
  messageScrollTime = millis();
  messageColorTime = millis();
  messageHeaderVisible = true;
  messageScrollPos = 0;
  messageColorIndex = 0;

  LOG("[Message] Starting message display mode");
  LOGF("[Message] Text: %s\n", messageText);

  // Clear screen for message mode
  lcd.clear();
  lastLine1[0] = '\0';
  lastLine2[0] = '\0';
}

void stopMessageMode() {
  messageMode = false;
  ledOff();
  lcd.clear();
  lastLine1[0] = '\0';
  lastLine2[0] = '\0';
  lastSecond = 255;  // Force time screen refresh
  LOG("[Message] Message display mode ended");
}

void updateMessageDisplay() {
  if (!messageMode) return;

  unsigned long now = millis();

  // Check if message duration expired (1 minute)
  if (now - messageStartTime >= MESSAGE_DURATION) {
    stopMessageMode();
    return;
  }

  // Blink "MESSAGE" header on line 1 (centered)
  if (now - messageBlinkTime >= MESSAGE_BLINK_INTERVAL) {
    messageBlinkTime = now;
    messageHeaderVisible = !messageHeaderVisible;

    lcd.setCursor(0, 0);
    if (messageHeaderVisible) {
      lcd.print("    MESSAGE     ");  // Centered on 16 chars
    } else {
      lcd.print("                ");  // Blank
    }
  }

  // Scroll message on line 2
  if (now - messageScrollTime >= MESSAGE_SCROLL_INTERVAL) {
    messageScrollTime = now;

    int msgLen = strlen(messageText);
    char scrollBuf[64];

    if (msgLen <= 16) {
      // No scrolling needed - center the text
      int padding = (16 - msgLen) / 2;
      snprintf(scrollBuf, 17, "%*s%s%*s", padding, "", messageText, 16 - msgLen - padding, "");
      lcd.setCursor(0, 1);
      lcd.print(scrollBuf);
    } else {
      // Create scrolling text with padding
      char paddedMsg[192];
      snprintf(paddedMsg, 192, "%s    %s", messageText, messageText);  // Loop the message

      // Extract 16-char window
      char display[17];
      strncpy(display, paddedMsg + messageScrollPos, 16);
      display[16] = '\0';

      lcd.setCursor(0, 1);
      lcd.print(display);

      // Advance scroll position
      messageScrollPos++;
      if (messageScrollPos >= msgLen + 4) {
        messageScrollPos = 0;
      }
    }
  }

  // Cycle through LED colors
  if (now - messageColorTime >= MESSAGE_COLOR_INTERVAL) {
    messageColorTime = now;
    messageColorIndex = (messageColorIndex + 1) % MESSAGE_COLOR_COUNT;
    ledSet(MESSAGE_COLORS[messageColorIndex], BRIGHT);
  }
}

// ============================================
// INITIALIZATION SEQUENCE
// ============================================

// Step 1: Init LCD - ORANGE
bool initLCD() {
  LOG("[Init] Step 1: LCD");
  ledStartBlink(COLOR_ORANGE, DULL, 300);

  Wire.begin(LCD_SDA_PIN, LCD_SCL_PIN);

  Wire.beginTransmission(LCD_ADDRESS);
  if (Wire.endTransmission() != 0) {
    LOG("[Init] LCD not found!");
    return false;
  }

  lcd.init();
  lcd.backlight();
  lcdShowForce("Scanning I2C...", "Address: 0x27");

  // Blink while "connecting"
  for (int i = 0; i < 4; i++) {
    ledUpdate();
    delay(250);
  }

  // Success: Bright Orange 1.5s
  ledSolid(COLOR_ORANGE, BRIGHT);
  lcdShowForce("Display Ready", "16x2 I2C OK");
  delay(1500);

  state.lcdReady = true;
  LOG("[Init] LCD Ready");
  return true;
}

// Step 2: WiFi - BLUE
bool initWiFi() {
  LOG("[Init] Step 2: WiFi");
  ledStartBlink(COLOR_BLUE, DULL, 300);

  char ssidDisplay[17];
  strncpy(ssidDisplay, WIFI_SSID, 10);
  ssidDisplay[10] = '\0';

  char line1[17];
  snprintf(line1, 17, "WiFi:%s", ssidDisplay);
  lcdShowForce(line1, "Connecting...");

  WiFi.mode(WIFI_STA);
  WiFi.setAutoReconnect(true);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 40) {
    delay(500);
    Serial.print(".");
    ledUpdate();
    attempts++;
  }
  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    WiFi.setSleep(false);
    esp_wifi_set_ps(WIFI_PS_NONE);

    // Success: Bright Blue 1.5s
    ledSolid(COLOR_BLUE, BRIGHT);
    lcdShowForce("WiFi Connected", WiFi.localIP().toString().c_str());
    delay(1500);

    state.wifiConnected = true;
    LOGF("[Init] WiFi Connected: %s\n", WiFi.localIP().toString().c_str());
    return true;
  }

  lcdShowForce("WiFi Failed!", "Check credentials");
  ledFlash(COLOR_RED, BRIGHT, 3, 200);
  delay(2000);
  return false;
}

// Step 3: Time Sync - YELLOW
bool initTime() {
  if (!state.wifiConnected) return false;

  LOG("[Init] Step 3: Time Sync");
  ledStartBlink(COLOR_YELLOW, DULL, 300);
  lcdShowForce("Syncing Clock...", NTP_SERVER_1);

  configTime(GMT_OFFSET, DST_OFFSET, NTP_SERVER_1, NTP_SERVER_2, NTP_SERVER_3);

  struct tm timeinfo;
  int attempts = 0;
  while (!getLocalTime(&timeinfo, 1000) && attempts < 10) {
    delay(500);
    ledUpdate();
    attempts++;
  }

  if (getLocalTime(&timeinfo)) {
    // Success: Bright Yellow 1.5s
    ledSolid(COLOR_YELLOW, BRIGHT);

    char dateLine[17];
    snprintf(dateLine, 17, "%02d/%02d %02d:%02d:%02d",
             timeinfo.tm_mday, timeinfo.tm_mon + 1,
             timeinfo.tm_hour, timeinfo.tm_min, timeinfo.tm_sec);
    lcdShowForce("Clock Synced", dateLine);
    delay(1500);

    state.timeSync = true;
    LOG("[Init] Time Synced");
    return true;
  }

  lcdShowForce("Time Sync Failed", "Will retry...");
  delay(1500);
  return false;
}

// Step 4: MQTT - MAGENTA
bool initMQTT() {
  if (!state.wifiConnected) return false;

  LOG("[Init] Step 4: MQTT");
  ledStartBlink(COLOR_MAGENTA, DULL, 300);
  lcdShowForce("MQTT Broker...", "HiveMQ Cloud");

  wifiClient.setInsecure();
  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
  mqtt.setCallback(onMqttMessage);
  mqtt.setBufferSize(MQTT_BUFFER_SIZE);

  String clientId = "esp32-" + String(random(0xffff), HEX);

  int attempts = 0;
  while (!mqtt.connected() && attempts < 5) {
    ledUpdate();
    if (mqtt.connect(clientId.c_str(), MQTT_USERNAME, MQTT_PASSWORD)) {
      break;
    }
    delay(1000);
    ledUpdate();
    attempts++;
  }

  if (mqtt.connected()) {
    mqtt.subscribe(MQTT_TOPIC_COMMANDS);

    // Success: Bright Magenta 1s
    ledSolid(COLOR_MAGENTA, BRIGHT);
    lcdShowForce("MQTT Connected", DEVICE_ID);
    delay(1000);

    // Then Bright Green 2s
    ledSolid(COLOR_GREEN, BRIGHT);
    lcdShowForce("MQTT Ready!", "Subscribed OK");
    delay(2000);

    state.mqttConnected = true;
    LOG("[Init] MQTT Connected");
    return true;
  }

  lcdShowForce("MQTT Failed!", "Check credentials");
  ledFlash(COLOR_RED, BRIGHT, 3, 200);
  delay(2000);
  return false;
}

// Step 5: All Ready
void initComplete() {
  LOG("[Init] All Systems Ready!");

  ledFlash(COLOR_GREEN, BRIGHT, 3, 150);
  ledSolid(COLOR_GREEN, BRIGHT);

  lcdShowForce("* System Ready *", "v2.6 All OK");
  delay(2000);

  state.allReady = true;
  sendHeartbeat();

  // LED OFF in normal mode
  ledOff();

  // Reset screen
  timers.screenChange = millis();
  currentScreen = 0;
  showingTimeScreen = true;
  lastLine1[0] = '\0';
  lastLine2[0] = '\0';
}

void initRelays() {
  LOG("[Init] Initializing Relays...");
  for (int i = 0; i < 4; i++) {
    pinMode(RELAY_PINS[i], OUTPUT);
    digitalWrite(RELAY_PINS[i], HIGH);
    state.relays[i] = false;
    LOGF("[Init] Relay %d (GPIO %d) = OFF\n", i+1, RELAY_PINS[i]);
  }
}

// ============================================
// SCREEN DISPLAY (No Flicker)
// ============================================
void showTimeScreen() {
  struct tm t;
  if (getLocalTime(&t)) {
    // Only update if second changed
    if (t.tm_sec != lastSecond) {
      lastSecond = t.tm_sec;

      // Convert to 12-hour format
      int hour12 = t.tm_hour % 12;
      if (hour12 == 0) hour12 = 12;  // 0 becomes 12
      const char* ampm = (t.tm_hour < 12) ? "AM" : "PM";

      char line1[17], line2[17];
      snprintf(line1, 17, "  %2d:%02d:%02d %s", hour12, t.tm_min, t.tm_sec, ampm);

      const char* days[] = {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};
      const char* months[] = {"Jan", "Feb", "Mar", "Apr", "May", "Jun",
                              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"};
      snprintf(line2, 17, "%s %02d %s %04d",
               days[t.tm_wday], t.tm_mday, months[t.tm_mon], t.tm_year + 1900);
      lcdShow(line1, line2);
    }
  }
}

void showWifiScreen() {
  char line1[17], line2[17];
  snprintf(line1, 17, "WiFi: %ddBm", WiFi.RSSI());
  snprintf(line2, 17, "MQTT: %s", state.mqttConnected ? "Connected" : "Disconn");
  lcdShow(line1, line2);
}

void showRelayScreen() {
  char line1[17], line2[17];
  snprintf(line1, 17, "L:%s F:%s",
           state.relays[0] ? "ON " : "OFF",
           state.relays[1] ? "ON " : "OFF");
  snprintf(line2, 17, "A:%s R:%s",
           state.relays[2] ? "ON " : "OFF",
           state.relays[3] ? "ON " : "OFF");
  lcdShow(line1, line2);
}

void updateScreen() {
  unsigned long now = millis();
  unsigned long elapsed = now - timers.screenChange;

  if (showingTimeScreen) {
    showTimeScreen();

    if (elapsed >= TIME_SCREEN_DURATION) {
      showingTimeScreen = false;
      currentScreen = 1;
      timers.screenChange = now;
      lastLine1[0] = '\0';
      lastLine2[0] = '\0';
    }
  } else {
    if (currentScreen == 1) {
      showWifiScreen();
    } else if (currentScreen == 2) {
      showRelayScreen();
    }

    if (elapsed >= STATUS_SCREEN_DURATION) {
      timers.screenChange = now;
      currentScreen++;
      lastLine1[0] = '\0';
      lastLine2[0] = '\0';

      if (currentScreen > 2) {
        currentScreen = 0;
        showingTimeScreen = true;
        lastSecond = 255;
      }
    }
  }
}

// ============================================
// MQTT HANDLERS
// ============================================
void onMqttMessage(char* topic, byte* payload, unsigned int length) {
  StaticJsonDocument<512> doc;
  DeserializationError err = deserializeJson(doc, payload, length);

  if (err) {
    LOGF("[MQTT] JSON parse error: %s\n", err.c_str());
    return;
  }

  const char* type = doc["type"];
  LOGF("[MQTT] Received: %s\n", type);

  // CYAN flash on receive
  ledFlash(COLOR_CYAN, BRIGHT, 2, 100);

  if (strcmp(type, "IMMEDIATE") == 0) {
    handleImmediate(doc);
  } else if (strcmp(type, "SCHEDULE") == 0) {
    handleSchedule(doc);
  } else if (strcmp(type, "CANCEL") == 0) {
    handleCancel(doc);
  } else if (strcmp(type, "STATUS") == 0) {
    sendHeartbeat();
  } else if (strcmp(type, "MESSAGE") == 0) {
    handleMessage(doc);
    return;  // Don't turn off LED - message mode manages it
  }

  ledOff();
}

void handleImmediate(JsonDocument& doc) {
  // FIXED: Use relay_number not relay
  int relay = doc["relay_number"] | doc["relay"].as<int>();
  const char* action = doc["action"];
  const char* cmdId = doc["command_id"];

  LOGF("[Immediate] Relay: %d, Action: %s, CmdId: %s\n", relay, action, cmdId);

  // relay_number: 0 means ALL relays
  if (relay == 0) {
    LOGF("[Immediate] ALL RELAYS -> %s\n", action);

    // Show on LCD
    ledSolid(COLOR_CYAN, BRIGHT);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("ALL DEVICES");
    lcd.setCursor(0, 1);
    lcd.print(strcmp(action, "on") == 0 ? "-> ON" : "-> OFF");

    // Execute on all 4 relays
    for (int r = 1; r <= 4; r++) {
      executeAction(r, action);
    }

    sendAck(cmdId, true, "All executed");
    delay(1000);
    return;
  }

  if (relay < 1 || relay > 4) {
    LOGF("[Immediate] ERROR: Invalid relay number %d\n", relay);
    sendAck(cmdId, false, "Invalid relay");
    return;
  }

  // Show device and action on LCD - CYAN
  ledSolid(COLOR_CYAN, BRIGHT);

  // Build info string for scrolling
  char info[48];
  snprintf(info, 48, "Immediate: %s -> %s", RELAY_NAMES[relay - 1], action);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Command Received");
  lcdScrollLine(1, info, 120);  // Fast scroll on line 2

  executeAction(relay, action);
  sendAck(cmdId, true, "Executed");
}

void handleSchedule(JsonDocument& doc) {
  const char* cmdId = doc["command_id"];

  if (scheduleCount >= MAX_SCHEDULES) {
    sendAck(cmdId, false, "Schedule full");
    return;
  }

  Schedule& s = schedules[scheduleCount];
  strncpy(s.id, cmdId, 39);
  s.id[39] = '\0';
  // FIXED: Use relay_number
  s.relay = doc["relay_number"] | doc["relay"].as<int>();
  strncpy(s.action, doc["action"], 7);
  s.action[7] = '\0';
  // FIXED: Backend sends "scheduled_time", not "execute_at"
  s.executeAt = doc["scheduled_time"] | doc["execute_at"].as<time_t>();
  s.active = true;
  s.countdownStarted = false;
  scheduleCount++;

  ledFlash(COLOR_CYAN, DULL, 2, 150);

  // Build schedule info string for scrolling
  struct tm* tm = localtime(&s.executeAt);

  // Convert to 12-hour format
  int hour12 = tm->tm_hour % 12;
  if (hour12 == 0) hour12 = 12;
  const char* ampm = (tm->tm_hour < 12) ? "AM" : "PM";

  // Get relay name (0 = ALL)
  const char* relayName = (s.relay == 0) ? "ALL" : RELAY_NAMES[s.relay - 1];

  char info[48];
  snprintf(info, 48, "%s -> %s @ %d:%02d %s",
           relayName, s.action,
           hour12, tm->tm_min, ampm);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Schedule Added");
  lcdScrollLine(1, info, 120);  // Fast scroll on line 2

  sendAck(cmdId, true, "Scheduled");

  // Debug: show current time vs scheduled time
  time_t now;
  time(&now);
  LOGF("[Schedule] Added: relay %d, scheduled_time=%ld, current_time=%ld, diff=%ld sec\n",
       s.relay, (long)s.executeAt, (long)now, (long)(s.executeAt - now));

  ledOff();
  lastLine1[0] = '\0';
  lastLine2[0] = '\0';
}

void handleCancel(JsonDocument& doc) {
  const char* cmdId = doc["command_id"];

  for (int i = 0; i < scheduleCount; i++) {
    if (strcmp(schedules[i].id, cmdId) == 0) {
      schedules[i].active = false;
      sendAck(cmdId, true, "Cancelled");
      return;
    }
  }
  sendAck(cmdId, false, "Not found");
}

void handleMessage(JsonDocument& doc) {
  const char* cmdId = doc["command_id"];
  const char* text = doc["message"];

  if (!text || strlen(text) == 0) {
    sendAck(cmdId, false, "Empty message");
    return;
  }

  LOGF("[Message] Received: %s\n", text);

  // Start message display mode
  startMessageMode(text);

  sendAck(cmdId, true, "Message displaying");
}

// ============================================
// ACTION EXECUTION
// ============================================
void executeAction(int relay, const char* action) {
  if (relay < 1 || relay > 4) {
    LOGF("[Relay] Invalid relay: %d\n", relay);
    return;
  }

  int idx = relay - 1;
  bool newState;

  if (strcmp(action, "on") == 0) {
    newState = true;
  } else if (strcmp(action, "off") == 0) {
    newState = false;
  } else if (strcmp(action, "toggle") == 0) {
    newState = !state.relays[idx];
  } else {
    LOGF("[Relay] Invalid action: %s\n", action);
    return;
  }

  state.relays[idx] = newState;
  digitalWrite(RELAY_PINS[idx], newState ? LOW : HIGH);

  LOGF("[Relay] %s (GPIO %d) = %s\n",
       RELAY_NAMES[idx], RELAY_PINS[idx],
       newState ? "ON" : "OFF");

  // Display result
  char line1[17], line2[17];
  snprintf(line1, 17, "%s", RELAY_NAMES[idx]);
  snprintf(line2, 17, "Switched %s", newState ? "ON" : "OFF");
  lcdShowForce(line1, line2);

  // GREEN BRIGHT 2 seconds, then OFF
  ledSolid(COLOR_GREEN, BRIGHT);
  delay(2000);
  ledOff();

  // Reset screen state
  lastLine1[0] = '\0';
  lastLine2[0] = '\0';
}

void executeScheduledAction(int relay, const char* action, const char* cmdId) {
  // relay=0 means ALL devices
  if (relay == 0) {
    for (int r = 1; r <= 4; r++) {
      executeAction(r, action);
    }
    sendExecuted(cmdId, 0, action);
  } else {
    executeAction(relay, action);
    sendExecuted(cmdId, relay, action);
  }
}

// ============================================
// SCHEDULE CHECK
// ============================================
void checkSchedules() {
  time_t now;
  time(&now);

  for (int i = 0; i < scheduleCount; i++) {
    Schedule& s = schedules[i];
    if (!s.active) continue;

    long diff = s.executeAt - now;

    if (diff <= 3 && diff > 0 && !s.countdownStarted) {
      s.countdownStarted = true;
      LOGF("[Schedule] Countdown for relay %d\n", s.relay);

      // 3 second RED rapid blink countdown
      const char* relayName = (s.relay == 0) ? "ALL" : RELAY_NAMES[s.relay - 1];

      for (int sec = diff; sec > 0; sec--) {
        ledStartBlink(COLOR_RED, BRIGHT, 100);

        char line1[17], line2[17];
        snprintf(line1, 17, "Action in %d...", sec);
        snprintf(line2, 17, "%s -> %s", relayName, s.action);
        lcdShowForce(line1, line2);

        unsigned long start = millis();
        while (millis() - start < 1000) {
          ledUpdate();
          delay(50);
        }
      }

      executeScheduledAction(s.relay, s.action, s.id);
      s.active = false;
    }
    else if (diff <= 0) {
      LOGF("[Schedule] Executing (past due) relay %d\n", s.relay);
      executeScheduledAction(s.relay, s.action, s.id);
      s.active = false;
    }
  }

  // Cleanup
  int writeIdx = 0;
  for (int i = 0; i < scheduleCount; i++) {
    if (schedules[i].active) {
      if (writeIdx != i) schedules[writeIdx] = schedules[i];
      writeIdx++;
    }
  }
  scheduleCount = writeIdx;
}

// ============================================
// MQTT MESSAGES
// ============================================
void sendHeartbeat() {
  StaticJsonDocument<512> doc;  // Increased from 256 to fit all relay data
  doc["type"] = "HEARTBEAT";
  doc["device_id"] = DEVICE_ID;
  doc["online"] = true;
  doc["wifi_rssi"] = WiFi.RSSI();
  doc["free_heap"] = ESP.getFreeHeap();
  doc["uptime"] = millis() / 1000;

  JsonArray relays = doc.createNestedArray("relays");
  for (int i = 0; i < 4; i++) {
    JsonObject r = relays.createNestedObject();
    r["number"] = i + 1;
    r["name"] = RELAY_NAMES[i];
    r["state"] = state.relays[i] ? "on" : "off";
  }

  char buffer[512];  // Increased from 256
  serializeJson(doc, buffer);
  mqtt.publish(MQTT_TOPIC_STATUS, buffer);
  LOG("[MQTT] Heartbeat sent");
}

void sendAck(const char* cmdId, bool success, const char* msg) {
  StaticJsonDocument<128> doc;
  doc["type"] = "ACK";
  doc["command_id"] = cmdId;
  doc["success"] = success;
  doc["message"] = msg;

  char buffer[128];
  serializeJson(doc, buffer);
  mqtt.publish(MQTT_TOPIC_ACK, buffer);
}

void sendExecuted(const char* cmdId, int relay, const char* action) {
  StaticJsonDocument<128> doc;
  doc["type"] = "EXECUTED";
  doc["command_id"] = cmdId;
  doc["relay"] = relay;
  doc["action"] = action;

  char buffer[128];
  serializeJson(doc, buffer);
  mqtt.publish(MQTT_TOPIC_STATUS, buffer);
}

// ============================================
// CONNECTION CHECK
// ============================================
void checkWiFi() {
  bool connected = (WiFi.status() == WL_CONNECTED);

  if (!connected && state.wifiConnected) {
    state.wifiConnected = false;
    state.mqttConnected = false;

    LOG("[WiFi] Lost!");
    ledStartBlink(COLOR_BLUE, DULL, 300);
    lcdShowForce("! WiFi Lost", "Reconnecting...");

    WiFi.disconnect();
    delay(1000);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  } else if (connected && !state.wifiConnected) {
    state.wifiConnected = true;
    WiFi.setSleep(false);
    esp_wifi_set_ps(WIFI_PS_NONE);

    ledSolid(COLOR_BLUE, BRIGHT);
    lcdShowForce("WiFi Restored", WiFi.localIP().toString().c_str());
    LOG("[WiFi] Reconnected");
    delay(1500);

    ledOff();
    lastLine1[0] = '\0';
    lastLine2[0] = '\0';
  }
}

void reconnectMQTT() {
  if (!state.wifiConnected || mqtt.connected()) return;

  LOG("[MQTT] Reconnecting...");
  ledStartBlink(COLOR_MAGENTA, DULL, 300);
  lcdShowForce("MQTT Reconnect", "Please wait...");

  String clientId = "esp32-" + String(random(0xffff), HEX);

  if (mqtt.connect(clientId.c_str(), MQTT_USERNAME, MQTT_PASSWORD)) {
    mqtt.subscribe(MQTT_TOPIC_COMMANDS);
    state.mqttConnected = true;

    // Magenta bright 1s
    ledSolid(COLOR_MAGENTA, BRIGHT);
    lcdShowForce("MQTT Connected", DEVICE_ID);
    delay(1000);

    // Green bright 2s
    ledSolid(COLOR_GREEN, BRIGHT);
    lcdShowForce("MQTT Ready!", "Subscribed OK");
    delay(2000);

    LOG("[MQTT] Reconnected");
    ledOff();
    lastLine1[0] = '\0';
    lastLine2[0] = '\0';
  } else {
    state.mqttConnected = false;
    LOGF("[MQTT] Failed rc=%d\n", mqtt.state());
  }
}

// ============================================
// SETUP
// ============================================
void setup() {
  Serial.begin(115200);
  delay(1000);

  LOG("\n========================================");
  LOG("Evolution Todo - IoT Controller v2.6");
  LOG("========================================\n");

  initRelays();

  if (!initLCD()) {
    LOG("[FATAL] LCD init failed!");
    ledStartBlink(COLOR_RED, BRIGHT, 200);
    while(1) { ledUpdate(); delay(10); }
  }

  initWiFi();
  initTime();
  initMQTT();
  initComplete();

  LOG("\n========================================");
  LOG("Setup Complete!");
  LOG("========================================\n");
}

// ============================================
// LOOP
// ============================================
void loop() {
  unsigned long now = millis();

  ledUpdate();

  if (now - timers.wifiCheck >= WIFI_CHECK_INTERVAL) {
    timers.wifiCheck = now;
    checkWiFi();
  }

  if (state.wifiConnected) {
    if (mqtt.connected()) {
      mqtt.loop();
      state.mqttConnected = true;
    } else {
      state.mqttConnected = false;
      if (now - timers.mqttReconnect >= MQTT_RECONNECT_INTERVAL) {
        timers.mqttReconnect = now;
        reconnectMQTT();
      }
    }
  }

  if (state.mqttConnected && (now - timers.heartbeat >= HEARTBEAT_INTERVAL)) {
    timers.heartbeat = now;
    sendHeartbeat();
  }

  if (state.timeSync && (now - timers.scheduleCheck >= SCHEDULE_CHECK_INTERVAL)) {
    timers.scheduleCheck = now;
    checkSchedules();
  }

  if (!state.timeSync && state.wifiConnected && (now - timers.ntpRetry >= NTP_RETRY_INTERVAL)) {
    timers.ntpRetry = now;
    initTime();
  }

  // Handle message display mode (takes priority over normal screens)
  if (messageMode) {
    updateMessageDisplay();
  } else if (state.allReady) {
    updateScreen();
  }
}
