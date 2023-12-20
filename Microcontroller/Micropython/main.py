import machine
from machine import I2C, Pin
from distance import *
import time
import uos

# need this UART to read from BME and be able to send data to local computer
uart = machine.UART(0, baudrate=115200)
uart.init(115200, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))
uos.dupterm(uart)
i2c=I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

while True:
    d = distance()
    print(d.ultra())
    