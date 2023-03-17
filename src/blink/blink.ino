// https://microkontroller.ru/esp32-projects/programmirovanie-modulya-esp32-s-pomoshhyu-arduino-ide/
// ESP32 dev module

int LED_BUILTIN = 2;
void setup() {
  pinMode (LED_BUILTIN, OUTPUT);
}
void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}
