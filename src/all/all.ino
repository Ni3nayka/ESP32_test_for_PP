const int S1 = 34;
const int S2 = 35;

#include "esp32-hal-ledc.h"
const int L1 = 33;
const int L2 = 32;
const int R1 = 25;
const int R2 = 26;
const int dt = 10;

#include <Wire.h>
 
void setup(){
  pinMode (S1, INPUT);
  pinMode (S2, INPUT);

  ledcSetup(0, 50, 8);
  ledcSetup(1, 50, 8);
  ledcSetup(2, 50, 8);
  ledcSetup(3, 50, 8);
  ledcAttachPin (L1, 0);
  ledcAttachPin (L2, 1);
  ledcAttachPin (R1, 2);
  ledcAttachPin (R2, 3);
  pinMode (L1, OUTPUT);
  pinMode (L2, OUTPUT);
  pinMode (R1, OUTPUT);
  pinMode (R2, OUTPUT);
  ledcWrite(0,0);
  ledcWrite(1,0);
  ledcWrite(2,0);
  ledcWrite(3,0);
  
  #ifdef __AVR_ATmega328P__
     Wire.begin();
  #else
     Wire.begin(22, 21); 
  #endif
     
  Wire.setClock(400000); // choose 400 kHz I2C rate

  Serial.begin(9600);
  while (!Serial);
  Serial.println("\nI2C Scanner");
  test_I2C();
} 

void loop(){
  // left motor forward
  for (int i = 0; i<255; i++) {
    ledcWrite(0,i);
    delay(dt);
    test_sensor();
  }
  for (int i = 255; i>=0; i--) {
    ledcWrite(0,i);
    delay(dt);
    test_sensor();
  }
  // left motor backward
  for (int i = 0; i<255; i++) {
    ledcWrite(1,i);
    delay(dt);
    test_sensor();
  }
  for (int i = 255; i>=0; i--) {
    ledcWrite(1,i);
    delay(dt);
    test_sensor();
  }
  // right motor forward
  for (int i = 0; i<255; i++) {
    ledcWrite(2,i);
    delay(dt);
    test_sensor();
  }
  for (int i = 255; i>=0; i--) {
    ledcWrite(2,i);
    delay(dt);
    test_sensor();
  }
  // right motor backward
  for (int i = 0; i<255; i++) {
    ledcWrite(3,i);
    delay(dt);
    test_sensor();
  }
  for (int i = 255; i>=0; i--) {
    ledcWrite(3,i);
    delay(dt);
    test_sensor();
  }
}

void test_sensor() {
  Serial.print(digitalRead(S1));
  Serial.print(" ");
  Serial.println(digitalRead(S2));
}

void test_I2C() {
    delay(3000);
  byte error, address;
    int nDevices;
 
    Serial.println("Scanning...");
 
    nDevices = 0;
    for(address = 1; address < 127; address++ ){
      //Serial.println(address);
        Wire.beginTransmission(address);
        error = Wire.endTransmission();
 
        if (error == 0){
            Serial.print("I2C device found at address 0x");
            if (address<16)
                Serial.print("0");
            Serial.print(address,HEX);
            Serial.println(" !");
 
            nDevices++;
        }
        else if (error==4) {
            Serial.print("Unknow error at address 0x");
            if (address<16)
                Serial.print("0");
            Serial.println(address,HEX);
        } 
    }
    if (nDevices == 0)
        Serial.println("No I2C devices found\n");
    else
        Serial.println("done\n");
 
    delay(5000);
}
