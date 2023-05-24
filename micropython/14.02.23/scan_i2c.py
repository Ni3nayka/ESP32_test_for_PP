from machine import I2C, Pin
i2c = I2C(0,sda=Pin(21), scl=Pin(22))
print('Scan i2c bus...')
devices = i2c.scan()
print(devices)
if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))

  for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))