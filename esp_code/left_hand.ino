#include <esp_now.h>
#include <WiFi.h>
#include <Wire.h>
#include "MPU6050.h"

MPU6050 mpu;

typedef struct struct_message {
  int flex[5];
  float gyro[3];
  float accel[3];
} struct_message;

struct_message leftData;

uint8_t rightHandMAC[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF}; // ⚠️ UPDATE with actual MAC of Right Hand ESP

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW Init Failed");
    return;
  }
  esp_now_add_peer(rightHandMAC, ESP_NOW_ROLE_CONTROLLER, 1, NULL, 0);
  mpu.initialize();
}

void loop() {
  // Read flex sensors
  for (int i = 0; i < 5; i++) {
    leftData.flex[i] = analogRead(i);  // A0~A4
  }

  // Read MPU
  mpu.getRotation(&leftData.gyro[0], &leftData.gyro[1], &leftData.gyro[2]);
  mpu.getAcceleration(&leftData.accel[0], &leftData.accel[1], &leftData.accel[2]);

  esp_now_send(rightHandMAC, (uint8_t *)&leftData, sizeof(leftData));
  delay(50);
}
