from machine import Pin
import socket

# network module is used to configure the WiFi connection.
# There are two WiFi interfaces, one is STA, and the other is AP.
import network
import dht

# esp contains specific functions related to ESP8266 and ESP32 modules
import esp
# turn off vendor OS debugging messages
esp.osdebug(None)

# run a garbage collector to save space in the flash memory
import gc
gc.collect()

# enable ESP8266 AP mode
# create instance of AP object
ap_if = network.WLAN(network.AP_IF)
ap_if.active(True)
ap_if.config(essid='MicroPython-AP', password='123456789')

# check if the connection is established
while ap_if.active() == False:
    pass

print('Connection successful')
print(ap_if.ifconfig())

sensor = dht.DHT11(Pin(5))
LED = Pin(4, Pin.OUT)

# define LED initial state
LED.off()