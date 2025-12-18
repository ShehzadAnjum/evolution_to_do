# ESP32/ESP32-S3 WiFi Troubleshooting Guide

## Overview
This skill documents common ESP32 WiFi issues and proven solutions, learned from debugging sessions.

## Common Disconnect Reason Codes

| Code | Name | Cause | Fix |
|------|------|-------|-----|
| 2 | AUTH_EXPIRE | Wrong password or auth timeout | Verify password, check router auth type |
| 4 | ASSOC_EXPIRE | Association timeout | Move closer to router, check signal |
| 5 | ASSOC_TOOMANY | Router client limit reached | Disconnect other devices |
| 8 | ASSOC_LEAVE | ESP left network | Normal during disconnect |
| 13 | MIC_FAILURE | Password mismatch | Check password character-by-character |
| 14/15 | HANDSHAKE_TIMEOUT | 4-way handshake failed | Password issue or WPA3 incompatibility |
| 200 | BEACON_TIMEOUT | Lost signal | Move closer, check for interference |
| 201 | NO_AP_FOUND | SSID not visible | Check SSID spelling, router broadcasting |
| 202 | AUTH_FAIL | Authentication rejected | Wrong password or MAC filtered |
| 204 | HANDSHAKE_TIMEOUT | Connection failed | General connection issue |

## Proven Working Configuration

```cpp
// In setup, BEFORE WiFi.begin():
WiFi.mode(WIFI_STA);
WiFi.setAutoReconnect(true);   // Let ESP handle basic reconnects
WiFi.persistent(false);        // Don't save to flash (prevents corruption)

// DO NOT USE - causes issues:
// esp_wifi_set_country()      // Can conflict with router country setting

// Register event handlers BEFORE WiFi.begin():
WiFi.onEvent(onWiFiConnected, WiFiEvent_t::ARDUINO_EVENT_WIFI_STA_CONNECTED);
WiFi.onEvent(onWiFiGotIP, WiFiEvent_t::ARDUINO_EVENT_WIFI_STA_GOT_IP);
WiFi.onEvent(onWiFiDisconnected, WiFiEvent_t::ARDUINO_EVENT_WIFI_STA_DISCONNECTED);

// Connect:
WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

// AFTER connection (in onWiFiGotIP handler):
WiFi.setSleep(false);  // CRITICAL: Disable power saving AFTER connection
```

## Event Handler Pattern

```cpp
void onWiFiGotIP(WiFiEvent_t event, WiFiEventInfo_t info) {
  Serial.println("WiFi connected, IP: " + WiFi.localIP().toString());
  wifiConnected = true;
  WiFi.setSleep(false);  // Disable sleep to prevent random disconnects
}

void onWiFiDisconnected(WiFiEvent_t event, WiFiEventInfo_t info) {
  wifiConnected = false;
  Serial.print("Disconnected, reason: ");
  Serial.println(info.wifi_sta_disconnected.reason);
  // Event handler + setAutoReconnect(true) will handle reconnection
}
```

## Reconnection Strategy

1. **First 2 attempts**: Use `WiFi.reconnect()` - fast, usually works
2. **Next attempts**: Use `WiFi.disconnect()` + `WiFi.begin()` - fresh start
3. **After 3-5 failures**: `ESP.restart()` - full reset

```cpp
if (wifiFailCount <= 2) {
  WiFi.reconnect();
} else if (wifiFailCount <= 5) {
  WiFi.disconnect();
  delay(1000);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
} else {
  ESP.restart();
}
```

## Things That DON'T Work (Avoid)

1. **`esp_wifi_set_country()`** - Conflicts with router country, causes AUTH_EXPIRE
2. **`esp_wifi_deinit()` + `esp_wifi_init()`** - Too aggressive, destabilizes stack
3. **`WiFi.setSleep(false)` before connection** - Must be called AFTER connected
4. **Polling `WiFi.status()` in tight loop** - Use event handlers instead
5. **Multiple `WiFi.begin()` calls without disconnect** - Causes "sta is connecting" error

## Router Compatibility Checklist

- [ ] WPA2-PSK (not WPA3 only)
- [ ] AES encryption (TKIP+AES or AES only)
- [ ] Channel 1-11 (avoid 12-13 for US region ESP32)
- [ ] 2.4GHz band (ESP32 doesn't support 5GHz)
- [ ] SSID broadcast enabled
- [ ] MAC filtering disabled (or ESP32 MAC whitelisted)
- [ ] Not at client limit

## Debugging Steps

1. **Add WiFi scan at startup** - Shows visible networks and signal strength
2. **Print disconnect reason codes** - Use the table above to diagnose
3. **Check password length** - `strlen(WIFI_PASSWORD)` should match expected
4. **Test with mobile hotspot** - Isolates router vs ESP32 issues
5. **Move ESP32 closer** - Eliminates signal strength issues

## Signal Strength Guide

| RSSI | Quality | Notes |
|------|---------|-------|
| -30 to -50 | Excellent | Best performance |
| -50 to -60 | Good | Reliable |
| -60 to -70 | Fair | May have occasional issues |
| -70 to -80 | Weak | Frequent disconnects possible |
| Below -80 | Poor | Unreliable, move closer |

## References

- [Random Nerd Tutorials - Reconnect ESP32](https://randomnerdtutorials.com/solved-reconnect-esp32-to-wifi/)
- [ESP32 Forum - WiFi Issues](https://esp32.com/viewtopic.php?t=25257)
- [GitHub arduino-esp32 Issues](https://github.com/espressif/arduino-esp32/issues/3362)
