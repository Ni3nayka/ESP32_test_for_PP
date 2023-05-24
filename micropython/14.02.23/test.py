from machine import I2C, Pin
from vl53l1x import VL53L1X
import time
i2c = I2C(0, sda=Pin(21), scl=Pin(22),freq=400000)
devices = i2c.scan()
print(devices,i2c)
distance = VL53L1X(i2c)
while True:
    print("range: mm ", distance.read())
    time.sleep_ms(50)