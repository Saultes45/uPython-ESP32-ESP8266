
##########################################
## BOOT.PY
##########################################

#------------ Import--------------------
from machine import Pin, I2C, RTC, Timer, PWM
import ssd1306
from time import sleep
import gc #garbage collector
gc.collect() #start garbage collection
import math #for position in the oled calculation

#------------ Parameters --------------------
oledWidth   = 128
oledHeight  = 64
identReadAddress = 9


start_oledTextPosition        = 0
oledTextPosition              = 0
max_oledTextPositionIncrement = 6
inc_oledTextPosition          = 10
max_oledTextPosition = max_oledTextPositionIncrement * inc_oledTextPosition


#------------ Pins assignment --------------------
#ESP8266 pin assignment
pin_oled_i2c = I2C(-1, scl=Pin(5), sda=Pin(4))


#------------ My functions--------------------
def OLED_i2cscan():
  print("Scanning i2c adresses")
  for cnt_dots in range(0,10):
    print(".")
    sleep(0.1)
  del cnt_dots  
    

  listOfi2cAdresses = pin_oled_i2c.scan()
  if len(listOfi2cAdresses) == 0:
    print("No I2C devices found on the specified bus")
    print("Check you wirering")
  else:
    print("Found " + str(len(listOfi2cAdresses)) + " I2C device(s)")
    print("Trying to identify them by reading from address: " + str(identReadAddress))
    for cnt_i2cAdresses in range(0,len(listOfi2cAdresses)):
      print("Trying " + str(listOfi2cAdresses[cnt_i2cAdresses]))    
      dataFromBus = pin_oled_i2c.readfrom(listOfi2cAdresses[cnt_i2cAdresses],identReadAddress)
      print(dataFromBus)
  print("End of search")

def OLED_clear():
  print("Clearing oled")
  for cnt_line in range(0,5):
    print(cnt_line)
    oled.text('_____', 0, cnt_line * inc_oledTextPosition)
    oled.show()
    sleep(1)
  
  print("Done clearing oled")

#------------ Objects construction --------------------
oled = ssd1306.SSD1306_I2C(oledWidth, oledHeight, pin_oled_i2c)


#------------ Main loop --------------------

def tick(pin):                # we will receive the timer object when being called
    pin.value(not pin.value())                # toggle the LED#


#led_top = Pin(2, mode=Pin.OUT) # enable GP16 as output to drive the LED
#tim=Timer(-1)
#tim.init(period=2000, mode=Timer.PERIODIC, callback=tick(led_top))

pwm2 = PWM(Pin(2), freq=10, duty=200) # create and configure in one go


OLED_i2cscan()


#--------------
#display boot
for cnt_boot in range(0,2):
  for cnt_dot in range(0,4):
    oled.fill(0)
    oled.show()
    if cnt_dot == 0:
      oled.text('Booting', math.floor(oledWidth/2)-35, math.floor(oledHeight/2)-2)
    elif cnt_dot == 1:
      oled.text('Booting.', math.floor(oledWidth/2)-35-4, math.floor(oledHeight/2)-2)
    elif cnt_dot == 2:
      oled.text('Booting..', math.floor(oledWidth/2)-35-2*4, math.floor(oledHeight/2)-2)
    elif cnt_dot == 3:
      oled.text('Booting...', math.floor(oledWidth/2)-35-3*4, math.floor(oledHeight/2)-2)
    
    
    oled.show()
    #sleep(0.1)


del cnt_boot
del cnt_dot
sleep(0)


#------------------
#Drawing the title bloc or cartouche drawing

rtc = RTC()
rtc.datetime((2014, 5, 1, 4, 13, 0, 0, 0))

#draw the h line
TB_lineNumber = 15
for cnt_dot in range (0, oledWidth-1):
  oled.pixel(cnt_dot, TB_lineNumber,1)
  
for cnt_dot in range (0, TB_lineNumber+1):
  oled.pixel(oledWidth - 20, cnt_dot,1)

del cnt_dot
  
oled.text(str(rtc.datetime()[0])+str(rtc.datetime()[1])+str(rtc.datetime()[2]), 2, 5)
oled.show()
sleep(1)

#--------------

oled.fill(1)
oled.show()
sleep(0.5)

oled.fill(0)
oled.show()
sleep(1)

oled.pixel(0,0,1)
oled.pixel(0,oledHeight-1,1)
oled.pixel(oledWidth-1,oledHeight-1,1)
oled.pixel(oledWidth-1,0,1)
oled.show()
sleep(5)

oled.fill(0)
oled.show()



oled.text('Line 1', 0,0)
oled.text('Line 2', 0,10)
oled.text('Line 3', 0,20)
oled.show()
sleep(5)

oled.fill(0)
oled.show()
oledInverted = False


#------------ Main loop --------------------

tim.deinit()
pwm2.deinit()


while True:
  print(oledTextPosition)
  oled.text('Hello, world ' + str(oledTextPosition), 0, oledTextPosition)
  oledTextPosition = oledTextPosition + inc_oledTextPosition
  if oledTextPosition > (max_oledTextPositionIncrement * inc_oledTextPosition):
    oledTextPosition = start_oledTextPosition
    oledInverted = not oledInverted
    oled.invert(oledInverted)
    oled.fill(0)
  oled.show()
  sleep(0.5)


