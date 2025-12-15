/*
 * Evolution Todo - IoT Controller
 *
 * ESP32-S3 firmware for controlling relays via MQTT
 * Receives commands from Evolution Todo backend
 * Stores schedules locally for offline operation
 *
 * Hardware:
 * - ESP32-S3-WROOM-1 DevKit
 * - 4-channel relay module (Active LOW)
 * - I2C 16x2 LCD display (optional)
 *
 * Author: Evolution Todo Project
 * Date: 2025-12-14
 */

#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <esp_wifi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Preferences.h>
#include <time.h>

// ============================================
// LCD Toggle - Set to false to disable LCD
// ============================================
#define LCD_ENABLED false

#if LCD_ENABLED
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#endif

#include "config.h"

// ============================================
// Global Objects
// ============================================
WiFiClientSecure espClient;
PubSubClient mqtt(espClient);
#if LCD_ENABLED
LiquidCrystal_I2C lcd(LCD_ADDRESS, 16, 2);
#endif
Preferences preferences;

// ============================================
// Relay State
// ============================================
const int relayPins[] = {RELAY_1_PIN, RELAY_2_PIN, RELAY_3_PIN, RELAY_4_PIN};
const char* relayNames[] = {RELAY_1_NAME, RELAY_2_NAME, RELAY_3_NAME, RELAY_4_NAME};
bool relayStates[] = {false, false, false, false};  // false = OFF, true = ON

// ============================================
// Schedule Storage (max 20 schedules)
// ============================================
#define MAX_SCHEDULES 20

struct Schedule {
  char commandId[40];     // UUID
  uint8_t relayNumber;    // 1-4
  uint8_t action;         // 0=off, 1=on, 2=toggle
  uint32_t executeAt;     // Unix timestamp
  char deviceName[20];    // For display
  bool active;            // Is this slot in use?
  bool executed;          // Already executed?
};

Schedule schedules[MAX_SCHEDULES];
int scheduleCount = 0;

// ============================================
// Timing
// ============================================
unsigned long lastHeartbeat = 0;
unsigned long lastScheduleCheck = 0;
unsigned long lastLcdUpdate = 0;
unsigned long lastNtpSync = 0;
bool timeInitialized = false;

// ============================================
// LCD Display State
// ============================================
int lcdDisplayMode = 0;  // 0=status, 1=next schedule, 2=time
unsigned long lcdModeChangeTime = 0;

// ============================================
// Function Declarations
// ============================================
void setupWiFi();
void setupMQTT();
void setupRelays();
void setupTime();
void mqttCallback(char* topic, byte* payload, unsigned int length);
void reconnectMQTT();
void setRelay(int relayNum, bool state);
void toggleRelay(int relayNum);
void processCommand(JsonDocument& doc);
void addSchedule(const char* cmdId, int relay, int action, uint32_t execTime, const char* name);
void cancelSchedule(const char* cmdId);
void checkSchedules();
void sendStatus();
void sendAck(const char* cmdId, bool success, const char* message);
void sendHeartbeat();
void saveSchedulesToNVS();
void loadSchedulesFromNVS();
String getTimeString();
String formatTime(uint32_t timestamp);
#if LCD_ENABLED
void setupLCD();
void updateLCD();
#endif

// ============================================
// Setup
// ============================================
void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("\n========================================");
  Serial.println("Evolution Todo - IoT Controller");
  Serial.println("========================================");

  // Initialize components
  setupRelays();
  #if LCD_ENABLED
  setupLCD();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Evolution Todo");
  lcd.setCursor(0, 1);
  lcd.print("IoT Controller");
  delay(2000);
  #endif

  setupWiFi();
  setupTime();
  setupMQTT();

  // Load saved schedules from NVS
  loadSchedulesFromNVS();

  #if LCD_ENABLED
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Ready!");
  lcd.setCursor(0, 1);
  lcd.print("Schedules: ");
  lcd.print(scheduleCount);
  delay(2000);
  #endif

  Serial.println("Setup complete!");
  Serial.println("Waiting for MQTT commands...");
}

// ============================================
// Main Loop
// ============================================
void loop() {
  // Maintain MQTT connection
  if (!mqtt.connected()) {
    reconnectMQTT();
  }
  mqtt.loop();

  unsigned long now = millis();

  // Check schedules every second
  if (now - lastScheduleCheck >= SCHEDULE_CHECK_MS) {
    lastScheduleCheck = now;
    if (timeInitialized) {
      checkSchedules();
    }
  }

  // Send heartbeat
  if (now - lastHeartbeat >= HEARTBEAT_INTERVAL_MS) {
    lastHeartbeat = now;
    sendHeartbeat();
  }

  // Update LCD display
  #if LCD_ENABLED
  if (now - lastLcdUpdate >= LCD_UPDATE_MS) {
    lastLcdUpdate = now;
    updateLCD();
  }
  #endif

  // Sync NTP periodically
  if (now - lastNtpSync >= NTP_SYNC_INTERVAL_MS) {
    lastNtpSync = now;
    configTime(GMT_OFFSET, DST_OFFSET, NTP_SERVER);
  }
}

// ============================================
// WiFi Setup
// ============================================
void setupWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(WIFI_SSID);

  #if LCD_ENABLED
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connecting WiFi");
  #endif

  WiFi.mode(WIFI_STA);

  // Set WiFi country for better compatibility
  wifi_country_t country = {
    .cc = "PK",        // Pakistan (change to your country code)
    .schan = 1,
    .nchan = 13,
    .policy = WIFI_COUNTRY_POLICY_MANUAL
  };
  esp_wifi_set_country(&country);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    #if LCD_ENABLED
    lcd.setCursor(attempts % 16, 1);
    lcd.print(".");
    #endif
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());

    #if LCD_ENABLED
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("WiFi Connected!");
    lcd.setCursor(0, 1);
    lcd.print(WiFi.localIP());
    delay(2000);
    #endif
  } else {
    Serial.println("\nWiFi connection failed!");
    #if LCD_ENABLED
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("WiFi Failed!");
    lcd.setCursor(0, 1);
    lcd.print("Offline Mode");
    delay(2000);
    #endif
  }
}

// ============================================
// MQTT Setup
// ============================================
void setupMQTT() {
  // Use insecure client for HiveMQ Cloud (skip cert verification for demo)
  espClient.setInsecure();

  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
  mqtt.setCallback(mqttCallback);
  mqtt.setBufferSize(1024);  // Increase buffer for JSON messages

  Serial.print("MQTT Broker: ");
  Serial.println(MQTT_BROKER);
}

void reconnectMQTT() {
  if (WiFi.status() != WL_CONNECTED) {
    return;  // Can't connect MQTT without WiFi
  }

  int attempts = 0;
  while (!mqtt.connected() && attempts < 3) {
    Serial.print("Connecting to MQTT...");

    String clientId = "ESP32-" + String(DEVICE_ID) + "-" + String(random(0xffff), HEX);

    if (mqtt.connect(clientId.c_str(), MQTT_USERNAME, MQTT_PASSWORD)) {
      Serial.println("connected!");

      // Subscribe to command topic
      mqtt.subscribe(MQTT_TOPIC_COMMANDS);
      Serial.print("Subscribed to: ");
      Serial.println(MQTT_TOPIC_COMMANDS);

      // Send initial status
      sendStatus();

    } else {
      Serial.print("failed, rc=");
      Serial.print(mqtt.state());
      Serial.println(" retrying in 5 seconds");
      delay(5000);
      attempts++;
    }
  }
}

// ============================================
// MQTT Callback
// ============================================
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message received [");
  Serial.print(topic);
  Serial.print("]: ");

  // Convert payload to string
  char message[length + 1];
  memcpy(message, payload, length);
  message[length] = '\0';
  Serial.println(message);

  // Parse JSON
  JsonDocument doc;
  DeserializationError error = deserializeJson(doc, message);

  if (error) {
    Serial.print("JSON parse error: ");
    Serial.println(error.c_str());
    return;
  }

  processCommand(doc);
}

// ============================================
// Process Command
// ============================================
void processCommand(JsonDocument& doc) {
  const char* type = doc["type"];
  const char* commandId = doc["command_id"] | "unknown";

  Serial.print("Command type: ");
  Serial.println(type);

  if (strcmp(type, "IMMEDIATE") == 0) {
    // Execute immediately
    int relay = doc["relay_number"];
    const char* action = doc["action"];

    if (relay >= 1 && relay <= 4) {
      if (strcmp(action, "on") == 0) {
        setRelay(relay, true);
      } else if (strcmp(action, "off") == 0) {
        setRelay(relay, false);
      } else if (strcmp(action, "toggle") == 0) {
        toggleRelay(relay);
      }
      sendAck(commandId, true, "Executed immediately");
      sendStatus();
    } else {
      sendAck(commandId, false, "Invalid relay number");
    }

  } else if (strcmp(type, "SCHEDULE") == 0) {
    // Add to schedule
    int relay = doc["relay_number"];
    const char* action = doc["action"];
    uint32_t execTime = doc["scheduled_time"];
    const char* deviceName = doc["device_name"] | relayNames[relay - 1];

    int actionNum = 0;
    if (strcmp(action, "on") == 0) actionNum = 1;
    else if (strcmp(action, "toggle") == 0) actionNum = 2;

    addSchedule(commandId, relay, actionNum, execTime, deviceName);
    sendAck(commandId, true, "Schedule added");

  } else if (strcmp(type, "CANCEL") == 0) {
    // Cancel scheduled command
    cancelSchedule(commandId);
    sendAck(commandId, true, "Schedule cancelled");

  } else if (strcmp(type, "SYNC_REQ") == 0) {
    // Send all schedules
    sendStatus();

  } else if (strcmp(type, "STATUS_REQ") == 0) {
    // Send current relay states
    sendStatus();

  } else {
    sendAck(commandId, false, "Unknown command type");
  }
}

// ============================================
// Relay Control
// ============================================
void setupRelays() {
  for (int i = 0; i < 4; i++) {
    pinMode(relayPins[i], OUTPUT);
    digitalWrite(relayPins[i], HIGH);  // Active LOW - HIGH = OFF
    relayStates[i] = false;
  }
  Serial.println("Relays initialized (all OFF)");
}

void setRelay(int relayNum, bool state) {
  if (relayNum < 1 || relayNum > 4) return;

  int idx = relayNum - 1;
  relayStates[idx] = state;

  // Active LOW: LOW = ON, HIGH = OFF
  digitalWrite(relayPins[idx], state ? LOW : HIGH);

  Serial.print("Relay ");
  Serial.print(relayNum);
  Serial.print(" (");
  Serial.print(relayNames[idx]);
  Serial.print("): ");
  Serial.println(state ? "ON" : "OFF");

  // Update LCD immediately
  #if LCD_ENABLED
  updateLCD();
  #endif
}

void toggleRelay(int relayNum) {
  if (relayNum < 1 || relayNum > 4) return;
  setRelay(relayNum, !relayStates[relayNum - 1]);
}

// ============================================
// Schedule Management
// ============================================
void addSchedule(const char* cmdId, int relay, int action, uint32_t execTime, const char* name) {
  // Find empty slot
  int slot = -1;
  for (int i = 0; i < MAX_SCHEDULES; i++) {
    if (!schedules[i].active) {
      slot = i;
      break;
    }
  }

  if (slot == -1) {
    Serial.println("Schedule storage full!");
    return;
  }

  strncpy(schedules[slot].commandId, cmdId, 39);
  schedules[slot].commandId[39] = '\0';
  schedules[slot].relayNumber = relay;
  schedules[slot].action = action;
  schedules[slot].executeAt = execTime;
  strncpy(schedules[slot].deviceName, name, 19);
  schedules[slot].deviceName[19] = '\0';
  schedules[slot].active = true;
  schedules[slot].executed = false;

  scheduleCount++;

  Serial.print("Schedule added: ");
  Serial.print(name);
  Serial.print(" at ");
  Serial.println(formatTime(execTime));

  saveSchedulesToNVS();
}

void cancelSchedule(const char* cmdId) {
  for (int i = 0; i < MAX_SCHEDULES; i++) {
    if (schedules[i].active && strcmp(schedules[i].commandId, cmdId) == 0) {
      schedules[i].active = false;
      scheduleCount--;
      Serial.print("Schedule cancelled: ");
      Serial.println(cmdId);
      saveSchedulesToNVS();
      return;
    }
  }
  Serial.print("Schedule not found: ");
  Serial.println(cmdId);
}

void checkSchedules() {
  time_t now;
  time(&now);

  for (int i = 0; i < MAX_SCHEDULES; i++) {
    if (schedules[i].active && !schedules[i].executed) {
      if (now >= schedules[i].executeAt) {
        // Execute this schedule
        Serial.print("Executing schedule: ");
        Serial.println(schedules[i].deviceName);

        int relay = schedules[i].relayNumber;
        switch (schedules[i].action) {
          case 0: setRelay(relay, false); break;  // OFF
          case 1: setRelay(relay, true); break;   // ON
          case 2: toggleRelay(relay); break;      // TOGGLE
        }

        // Mark as executed
        schedules[i].executed = true;
        schedules[i].active = false;
        scheduleCount--;

        // Send execution confirmation
        JsonDocument doc;
        doc["type"] = "EXECUTED";
        doc["command_id"] = schedules[i].commandId;
        doc["relay_number"] = relay;
        doc["state"] = relayStates[relay - 1] ? "on" : "off";
        doc["executed_at"] = (long)now;
        doc["success"] = true;

        char buffer[256];
        serializeJson(doc, buffer);
        mqtt.publish(MQTT_TOPIC_STATUS, buffer);

        saveSchedulesToNVS();
      }
    }
  }
}

// ============================================
// MQTT Messages
// ============================================
void sendStatus() {
  JsonDocument doc;
  doc["type"] = "STATUS";
  doc["device_id"] = DEVICE_ID;
  doc["device_name"] = DEVICE_NAME;

  JsonArray relays = doc["relays"].to<JsonArray>();
  for (int i = 0; i < 4; i++) {
    JsonObject relay = relays.add<JsonObject>();
    relay["number"] = i + 1;
    relay["name"] = relayNames[i];
    relay["state"] = relayStates[i] ? "on" : "off";
  }

  doc["schedule_count"] = scheduleCount;
  doc["wifi_rssi"] = WiFi.RSSI();

  time_t now;
  time(&now);
  doc["timestamp"] = (long)now;

  char buffer[512];
  serializeJson(doc, buffer);
  mqtt.publish(MQTT_TOPIC_STATUS, buffer);

  Serial.println("Status sent");
}

void sendAck(const char* cmdId, bool success, const char* message) {
  JsonDocument doc;
  doc["type"] = "ACK";
  doc["command_id"] = cmdId;
  doc["success"] = success;
  doc["message"] = message;

  time_t now;
  time(&now);
  doc["timestamp"] = (long)now;

  char buffer[256];
  serializeJson(doc, buffer);
  mqtt.publish(MQTT_TOPIC_ACK, buffer);
}

void sendHeartbeat() {
  JsonDocument doc;
  doc["type"] = "HEARTBEAT";
  doc["device_id"] = DEVICE_ID;
  doc["uptime_ms"] = millis();
  doc["wifi_rssi"] = WiFi.RSSI();
  doc["free_heap"] = ESP.getFreeHeap();
  doc["schedule_count"] = scheduleCount;

  time_t now;
  time(&now);
  doc["timestamp"] = (long)now;

  char buffer[256];
  serializeJson(doc, buffer);
  mqtt.publish(MQTT_TOPIC_STATUS, buffer);

  Serial.println("Heartbeat sent");
}

// ============================================
// LCD Display
// ============================================
#if LCD_ENABLED
void setupLCD() {
  Wire.begin(LCD_SDA_PIN, LCD_SCL_PIN);
  lcd.init();
  lcd.backlight();
  Serial.println("LCD initialized");
}

void updateLCD() {
  lcd.clear();

  // Line 1: Current time and connection status
  lcd.setCursor(0, 0);
  if (timeInitialized) {
    lcd.print(getTimeString());
  } else {
    lcd.print("No Time Sync");
  }

  // Connection indicator
  lcd.setCursor(14, 0);
  if (mqtt.connected()) {
    lcd.print("OK");
  } else if (WiFi.status() == WL_CONNECTED) {
    lcd.print("WF");  // WiFi only
  } else {
    lcd.print("--");  // Offline
  }

  // Line 2: Relay states
  lcd.setCursor(0, 1);
  for (int i = 0; i < 4; i++) {
    lcd.print(i + 1);
    lcd.print(":");
    lcd.print(relayStates[i] ? "ON " : "OFF");
    if (i < 3) lcd.print(" ");
  }
}
#endif

// ============================================
// NVS Storage
// ============================================
void saveSchedulesToNVS() {
  preferences.begin("schedules", false);

  // Save schedule count
  preferences.putInt("count", scheduleCount);

  // Save each active schedule
  int savedCount = 0;
  for (int i = 0; i < MAX_SCHEDULES && savedCount < scheduleCount; i++) {
    if (schedules[i].active) {
      String key = "sch_" + String(savedCount);

      // Pack schedule into bytes
      uint8_t data[64];
      memcpy(data, schedules[i].commandId, 40);
      data[40] = schedules[i].relayNumber;
      data[41] = schedules[i].action;
      memcpy(data + 42, &schedules[i].executeAt, 4);
      memcpy(data + 46, schedules[i].deviceName, 18);

      preferences.putBytes(key.c_str(), data, 64);
      savedCount++;
    }
  }

  preferences.end();
  Serial.print("Saved ");
  Serial.print(savedCount);
  Serial.println(" schedules to NVS");
}

void loadSchedulesFromNVS() {
  preferences.begin("schedules", true);  // Read-only

  scheduleCount = preferences.getInt("count", 0);

  for (int i = 0; i < scheduleCount && i < MAX_SCHEDULES; i++) {
    String key = "sch_" + String(i);

    uint8_t data[64];
    if (preferences.getBytes(key.c_str(), data, 64) == 64) {
      memcpy(schedules[i].commandId, data, 40);
      schedules[i].relayNumber = data[40];
      schedules[i].action = data[41];
      memcpy(&schedules[i].executeAt, data + 42, 4);
      memcpy(schedules[i].deviceName, data + 46, 18);
      schedules[i].deviceName[19] = '\0';
      schedules[i].active = true;
      schedules[i].executed = false;
    }
  }

  preferences.end();
  Serial.print("Loaded ");
  Serial.print(scheduleCount);
  Serial.println(" schedules from NVS");
}

// ============================================
// Time Functions
// ============================================
void setupTime() {
  #if LCD_ENABLED
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Syncing time...");
  #endif

  configTime(GMT_OFFSET, DST_OFFSET, NTP_SERVER);

  Serial.print("Waiting for NTP time sync...");

  int attempts = 0;
  time_t now = 0;
  while (now < 1700000000 && attempts < 20) {  // Wait for valid time (after Nov 2023)
    delay(500);
    time(&now);
    Serial.print(".");
    attempts++;
  }

  if (now > 1700000000) {
    timeInitialized = true;
    Serial.println("\nTime synchronized!");
    Serial.print("Current time: ");
    Serial.println(getTimeString());

    #if LCD_ENABLED
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Time synced!");
    lcd.setCursor(0, 1);
    lcd.print(getTimeString());
    delay(2000);
    #endif
  } else {
    Serial.println("\nTime sync failed!");
    #if LCD_ENABLED
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Time sync fail");
    lcd.setCursor(0, 1);
    lcd.print("Using local");
    delay(2000);
    #endif
  }
}

String getTimeString() {
  time_t now;
  time(&now);
  struct tm* timeinfo = localtime(&now);

  char buffer[20];
  sprintf(buffer, "%02d:%02d:%02d",
          timeinfo->tm_hour,
          timeinfo->tm_min,
          timeinfo->tm_sec);
  return String(buffer);
}

String formatTime(uint32_t timestamp) {
  time_t t = timestamp;
  struct tm* timeinfo = localtime(&t);

  char buffer[20];
  sprintf(buffer, "%02d:%02d %02d/%02d",
          timeinfo->tm_hour,
          timeinfo->tm_min,
          timeinfo->tm_mday,
          timeinfo->tm_mon + 1);
  return String(buffer);
}
