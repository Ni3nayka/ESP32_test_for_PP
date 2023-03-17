// https://habr.com/ru/post/404685/

#include "esp32-hal-ledc.h"

const int L1 = 33;
const int L2 = 32;
const int R1 = 25;
const int R2 = 26;

const int dt = 10;

void setup() {
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
  
  Serial.begin(9600);
}
void loop() {
  // left motor forward
  for (int i = 0; i<255; i++) {
    ledcWrite(0,i);
    delay(dt);
    Serial.println(i);
  }
  for (int i = 255; i>=0; i--) {
    ledcWrite(0,i);
    delay(dt);
    Serial.println(i);
  }
  // left motor backward
  for (int i = 0; i<255; i++) {
    ledcWrite(1,i);
    delay(dt);
    Serial.println(i);
  }
  for (int i = 255; i>=0; i--) {
    ledcWrite(1,i);
    delay(dt);
    Serial.println(i);
  }
  // right motor forward
  for (int i = 0; i<255; i++) {
    ledcWrite(2,i);
    delay(dt);
    Serial.println(i);
  }
  for (int i = 255; i>=0; i--) {
    ledcWrite(2,i);
    delay(dt);
    Serial.println(i);
  }
  // right motor backward
  for (int i = 0; i<255; i++) {
    ledcWrite(3,i);
    delay(dt);
    Serial.println(i);
  }
  for (int i = 255; i>=0; i--) {
    ledcWrite(3,i);
    delay(dt);
    Serial.println(i);
  }
}
