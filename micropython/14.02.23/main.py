from MX1508 import *
from VL53L0X import *
from tcs34725 import *
from time import sleep_ms,sleep
from machine import Pin, I2C
import uasyncio as asio
from neopixel import NeoPixel
import aioespnow
import network

## esp_err_t gpio_set_direction(gpio_num_t 3, gpio_mode_t GPIO_MODE_OUTPUT)
i2c_bus = I2C(0, sda=Pin(14), scl=Pin(12))
tof = VL53L0X(i2c_bus)
i2c_bus1 = I2C(1, sda=Pin(2), scl=Pin(15))
tcs = TCS34725(i2c_bus1)
tcs.gain(4)
tcs.integration_time(80)
R_m_pin = Pin(32, Pin.IN)
L_m_pin = Pin(33, Pin.IN)
motor_L = MX1508(3, 21)
motor_R = MX1508(19, 18)
Sp=512
R_W_count,W_count,col_id,col_id_l,direct,di,dist,busy,busy_col,col_sel=0,0,0,0,0,0,500,0,0,5
NUM_OF_LED = 2
np = NeoPixel(Pin(13), NUM_OF_LED)
color=['Red','Yellow','White','Green','Black','Cyan','Blue','Magenta']
dir_move=['Stop','Forward','Left','Right','Reverse']
Lt = 60
debug = 0

network.WLAN(network.STA_IF).active(True)
e = aioespnow.AIOESPNow()  # Returns AIOESPNow enhanced with async support
e.active(True)
# peer = b'\xC8\xF0\x9E\x52\x66\x0C' #C8F09E52660C
# #'\\x'+mac[0:2]+'\\x'+mac[2:4]+'\\x'+mac[4:6]+'\\x'+mac[6:8]+'\\x'+mac[8:10]+'\\x'+mac[10:12]
# e.add_peer(peer)
# peer = b'\xC8\xF0\x9E\x4E\x9C\xA8' #C8F09E4E9CA8
# e.add_peer(peer)

motor_R.forward(Sp)
motor_L.forward(Sp)

def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    # h, s, v = hue, saturation, value
    cmax = max(r, g, b)    # maximum of r, g, b
    cmin = min(r, g, b)    # minimum of r, g, b
    diff = cmax-cmin       # diff of cmax and cmin.
    if cmax == cmin: 
        h = 0
    elif cmax == r: 
        h = (60 * ((g - b) / diff) + 360) % 360
    elif cmax == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    elif cmax == b:
        h = (60 * ((r - g) / diff) + 240) % 360
    if cmax == 0:
        s = 0
    else:
        s = (diff / cmax) * 100
    v = cmax * 100
    return h, s, v

def R_W_int(pin):
    global W_count,R_W_count
    W_count+=1
    R_W_count+=1
    
def L_W_int(pin):
    global W_count
    W_count-=1
   
R_m_pin.irq(trigger=Pin.IRQ_FALLING |Pin.IRQ_RISING , handler=R_W_int)
L_m_pin.irq(trigger=Pin.IRQ_FALLING |Pin.IRQ_RISING , handler=L_W_int)

async def synch(int_ms):
    while True:
        await asio.sleep_ms(int_ms)
        if direct==0: # движение вперед
            if W_count>0:
                motor_R.forward(0)
                motor_L.forward(Sp)
            elif W_count<0:
                motor_R.forward(Sp)
                motor_L.forward(0)
            else:
                motor_R.forward(Sp)
                motor_L.forward(Sp)
        elif direct==1: # поворот направо
            if W_count>0:
                motor_R.forward(0)
                motor_L.reverse(Sp)
            elif W_count<0:
                motor_R.forward(Sp)
                motor_L.reverse(0)
            else:
                motor_R.forward(Sp)
                motor_L.reverse(Sp)
        elif direct==2: # поворот налево
            if W_count>0:
                motor_R.reverse(0)
                motor_L.forward(Sp)
            elif W_count<0:
                motor_R.reverse(Sp)
                motor_L.forward(0)
            else:
                motor_R.reverse(Sp)
                motor_L.forward(Sp)        
        elif direct==3: # движение назад
            if W_count>0:
                motor_R.reverse(0)
                motor_L.reverse(Sp)
            elif W_count<0:
                motor_R.reverse(Sp)
                motor_L.reverse(0)
            else:
                motor_R.reverse(Sp)
                motor_L.reverse(Sp)
        elif direct==-1: # остановка
            motor_R.reverse(0)
            motor_L.reverse(0)

async def W_sp(int_ms): # устанавливем направление движения
    global R_W_count,dist,direct
    while True:
        await asio.sleep_ms(int_ms)
        await color_det()
        await dist_det()
        if 150<dist<250: di=1
        elif dist<150: di=2
        else: di=0
        if (not busy) & (not busy_col):
            if di==1:
                await asio.sleep_ms(2000)
                await dist_det()
                if 150<dist<250:
                    if dist%2:
                        direct=1
                    else:
                        direct=2
                        await move(8)
            elif di==2:
                await asio.sleep_ms(2000)
                await dist_det()
                if dist<150:
                    direct=3
                    await move(16)
            else:
                direct=0
        if  col_id==4: #col_id_l==col_id &
            direct=3
            await move(4)
            direct=2
            await move(8)
        if  col_id==col_sel:#col_id_l==col_id &
            direct=-1
            busy_col=1
        else:
            motor_R.reverse(Sp)
            motor_L.forward(Sp)
            busy_col=0
            
async def move(turn):
    global R_W_count,busy
    busy=1
    R_W_count=0    
    while R_W_count<turn:   
        await asio.sleep_ms(0)
    busy=0
    
async def dist_det():
    global dist
    tof.start()
    dist=tof.read()
    tof.stop()
    if debug:
        print('Distance is {}. W_count {}'.format(dist   ,W_count))

async def color_det():
    global col_id,col_id_l
    rgb=tcs.read(1)
    r,g,b=rgb[0],rgb[1],rgb[2]
    print("r =", r)
    print("g =", g)
    print("b =", b)
    h,s,v=rgb_to_hsv(r,g,b)
    if 0<h<60:
        col_id_l=col_id
        col_id=0
    elif 61<h<120:
        col_id_l=col_id
        col_id=1
    elif 121<h<180:
        if v>100:
            col_id_l=col_id
            col_id=2
        elif 25<v<100:
            col_id_l=col_id
            col_id=3
        elif v<25:
            col_id_l=col_id
            col_id=4
    elif 181<h<240:
        if v>40:
            col_id_l=col_id
            col_id=5
        else:
            col_id_l=col_id
            col_id=6
    elif 241<h<360:
        col_id_l=col_id
        col_id=7 
#     if debug:
#         print('Color is {}. R:{} G:{} B:{} H:{:.0f} S:{:.0f} V:{:.0f}'.format(color[col_id],r,g,b,h,s,v))
    
async def LED_cont(int_ms):
    while 1:
        await asio.sleep_ms(int_ms)
        if col_id==0: # Красный
            np[0]=(Lt,0,0)
        elif col_id==1: # Yellow
            np[0]=(Lt,Lt,0)
        elif col_id==2: # White
            np[0]=(Lt,Lt,Lt)
        elif col_id==3: # Green
            np[0]=(0,Lt,0)
        elif col_id==4: # Black?
            np[0]=(0,0,0)
            np.write()
            await asio.sleep_ms(300)
            np[0]=(Lt,0,0) # Для чего???
            np.write()
            await asio.sleep_ms(300)
        elif col_id==5: # Голубой
            np[0]=(0,Lt,Lt)
        elif col_id==6: # Синий
            np[0]=(0,0,Lt) 
        elif col_id==7: # Фиолетовый
            np[0]=(Lt,0,Lt)
        if di==0: # Светофорчик
            np[1]=(0,Lt,0)
        elif di==1:
            np[1]=(Lt,Lt,0)
        elif di==2:
            np[1]=(Lt,0,0)
        np.write()

async def send(e, period):
    while 1:
        await e.asend(color[col_id]+' '+dir_move[1+direct]+' '+str(dist)) #
        await asio.sleep_ms(period)
        
async def resive(e,int_ms):
    global col_sel
    while 1:
        async for mac, msg in e:
            col_sel=int.from_bytes(msg,'big')-48
            #print(color[col_sel])
            await asio.sleep_ms(int_ms)
        

loop = asio.get_event_loop()
loop.create_task(synch(1))
loop.create_task(W_sp(100))
##loop.create_task(LED_cont(100))
##loop.create_task(send(e,100))
##loop.create_task(resive(e,100))
loop.run_forever()
    