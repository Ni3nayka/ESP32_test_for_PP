// https://robotchip.ru/i2c-skaner-na-arduino/

/*
Тестировалось на Arduino IDE 1.8.5
Дата тестирования 26.10.2017г.
*/ 

#include <Wire.h>
 
void setup(){
  #ifdef __AVR_ATmega328P__
     Wire.begin();
  #else
     Wire.begin(22, 21); 
  #endif
     
  Wire.setClock(400000); // choose 400 kHz I2C rate

  Serial.begin(9600);
  while (!Serial);
  Serial.println("\nI2C Scanner");
} 

void loop(){
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
