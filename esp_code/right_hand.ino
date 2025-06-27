#include <esp_now.h>
#include <WiFi.h>
#include <Wire.h>
#include "BluetoothSerial.h"
#include "MPU6050.h"

MPU6050 mpu;
BluetoothSerial SerialBT;

typedef struct struct_message {
  int flex[5];
  float gyro[3];
  float accel[3];
} struct_message;

struct_message leftData;
struct_message rightData;

bool hasLeftData = false;

void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&leftData, incomingData, sizeof(leftData));
  hasLeftData = true;
}

void setup() {
  Serial.begin(115200);
  SerialBT.begin("Handspeak_Glove");
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  esp_now_init();
  esp_now_register_recv_cb(OnDataRecv);

  mpu.initialize();
}

void loop() {
  // Right hand flex sensors
  for (int i = 0; i < 5; i++) {
    rightData.flex[i] = analogRead(i);  // A0~A4
  }

  // Right hand MPU
  mpu.getRotation(&rightData.gyro[0], &rightData.gyro[1], &rightData.gyro[2]);
  mpu.getAcceleration(&rightData.accel[0], &rightData.accel[1], &rightData.accel[2]);

  if (hasLeftData) {
    String output = "";

    // Flex: Left + Right
    for (int i = 0; i < 5; i++) output += String(leftData.flex[i]) + ",";
    for (int i = 0; i < 5; i++) output += String(rightData.flex[i]) + ",";

    // Gyro+Accel Left
    for (int i = 0; i < 3; i++) output += String(leftData.gyro[i], 2) + ",";
    for (int i = 0; i < 3; i++) output += String(leftData.accel[i], 2) + ",";

    // Gyro+Accel Right
    for (int i = 0; i < 3; i++) output += String(rightData.gyro[i], 2) + ",";
    for (int i = 0; i < 3; i++) output += String(rightData.accel[i], 2);

    SerialBT.println(output);  // 🚀 Send to PC
    hasLeftData = false;
  }

  delay(50);
}
