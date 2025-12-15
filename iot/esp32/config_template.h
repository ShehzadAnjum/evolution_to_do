/*
 * Evolution Todo - IoT Configuration Template
 *
 * INSTRUCTIONS:
 * 1. Copy this file to 'config.h'
 * 2. Fill in your WiFi and MQTT credentials
 * 3. NEVER commit config.h to git (it's in .gitignore)
 */

#ifndef CONFIG_H
#define CONFIG_H

// ============================================
// WiFi Configuration
// ============================================
#define WIFI_SSID     "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

// ============================================
// MQTT Configuration (HiveMQ Cloud)
// ============================================
#define MQTT_BROKER   "your-cluster.hivemq.cloud"  // e.g., "abc123.s1.eu.hivemq.cloud"
#define MQTT_PORT     8883                          // TLS port
#define MQTT_USERNAME "your_username"
#define MQTT_PASSWORD "your_password"

// ============================================
// Device Configuration
// ============================================
#define DEVICE_ID     "esp32-home"                  // Unique device identifier
#define DEVICE_NAME   "Home Controller"             // Friendly name for display

// ============================================
// MQTT Topics (auto-generated from DEVICE_ID)
// ============================================
#define MQTT_TOPIC_BASE     "evolution-todo/devices/"
#define MQTT_TOPIC_COMMANDS MQTT_TOPIC_BASE DEVICE_ID "/commands"
#define MQTT_TOPIC_STATUS   MQTT_TOPIC_BASE DEVICE_ID "/status"
#define MQTT_TOPIC_ACK      MQTT_TOPIC_BASE DEVICE_ID "/ack"

// ============================================
// Hardware Pin Configuration
// ============================================
// Relay pins (Active LOW - send LOW to turn ON)
#define RELAY_1_PIN   4   // Living Room Light
#define RELAY_2_PIN   5   // Fan
#define RELAY_3_PIN   6   // Aquarium Light
#define RELAY_4_PIN   7   // Available

// I2C LCD pins
#define LCD_SDA_PIN   8
#define LCD_SCL_PIN   9
#define LCD_ADDRESS   0x27  // Common addresses: 0x27 or 0x3F

// Built-in LED (ESP32-S3 has RGB LED on GPIO 48)
#define LED_PIN       48

// ============================================
// Device Names (for display and messages)
// ============================================
#define RELAY_1_NAME  "Light"
#define RELAY_2_NAME  "Fan"
#define RELAY_3_NAME  "Aquarium"
#define RELAY_4_NAME  "Relay 4"

// ============================================
// Timing Configuration
// ============================================
#define HEARTBEAT_INTERVAL_MS   60000   // Send heartbeat every 60 seconds
#define SCHEDULE_CHECK_MS       1000    // Check schedules every second
#define LCD_UPDATE_MS           5000    // Update LCD display every 5 seconds
#define NTP_SYNC_INTERVAL_MS    3600000 // Sync NTP every hour

// ============================================
// NTP Configuration
// ============================================
#define NTP_SERVER    "pool.ntp.org"
#define GMT_OFFSET    18000             // Pakistan: UTC+5 = 5*3600 = 18000
#define DST_OFFSET    0                 // No daylight saving

#endif // CONFIG_H
