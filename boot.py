try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import esp32
#esp.osdebug(None)

import gc #garbage collector
gc.collect()

ssid = 'SPARK-DMU6GG'
password = 'UUQYXW2UDZ'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass


print('Connection successful')
print(station.ifconfig())

led = Pin(2, Pin.OUT)

import machine

machine.freq()  # get the current frequency of the CPU
machine.freq(240000000) 