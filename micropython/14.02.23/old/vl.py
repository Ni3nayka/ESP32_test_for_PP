from time import sleep_ms
from machine import Pin, I2C
from vl53l0x import *
#from VL53L0X import *
i2c_bus = I2C(0, sda=Pin(21), scl=Pin(22))
#sleep_ms(1000)
tof = VL53L0X(i2c_bus)

while True:
    
# Start ranging
    tof.start()
    tof.read()
    print(tof.read())
    tof.stop()