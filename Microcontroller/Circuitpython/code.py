import time
import usb_cdc
serial = usb_cdc.data # get the serial port object

#usb_cdc.enable(console=True, data=True) # enable the serial port
uart = usb_cdc.Serial()

s = bytearray("hello\n\r".encode())

while True:
    uart.write(s)
    time.sleep(1)