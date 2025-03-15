#include <SoftwareSerial.h>

// Define Bluetooth module TX/RX pins
SoftwareSerial Bluetooth(10, 11); // TX on pin 10, RX on pin 11

// Define sensor pins
const int thumbPin = A0;
const int index1Pin = A1;
const int index2Pin = A2;
const int middle1Pin = A3;
const int middle2Pin = A4;

void setup() {
    Serial.begin(9600);      // Serial monitor (USB)
    Bluetooth.begin(9600);   // Bluetooth module communication
}

void loop() {
    // Read sensor values
    int thumb = analogRead(thumbPin);
    int index1 = analogRead(index1Pin);
    int index2 = analogRead(index2Pin);
    int middle1 = analogRead(middle1Pin);
    int middle2 = analogRead(middle2Pin);

    // Format according to OpenGloves driver: "AxxxBxxxCxxxDxxxExxx\n"
    String dataString = "A" + String(thumb) + 
                        "B" + String(index1) + 
                        "C" + String(index2) + 
                        "D" + String(middle1) + 
                        "E" + String(middle2) + "\n";

    // Send data via Serial (USB) for debugging
    Serial.print(dataString);
    
    // Send data via Bluetooth
    Bluetooth.print(dataString);

    delay(10); // Small delay for stability
}
