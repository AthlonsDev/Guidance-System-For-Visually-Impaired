import pygatt # pygatt is a Python 2.x and 3.x module that allows you to communicate with Bluetooth LE devices.
import binascii # This module contains a number of methods to convert between binary and various ASCII-encoded binary representations.
import time

pico_uuid = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
mac = "d8:3a:dd:5c:49:ab"

#define the MAC address and UUID of the target deviec and characteristic
MAC = mac # MAC address is a unique identifier assigned to a Bluetooth device during the manufacturing process.
UUID = pico_uuid # UUID is a 128-bit number used to uniquely identify information.

# define exadecimal command to send
command_str = "toggle" # toggle is a command to turn on/off the LED
hex_command = binascii.hexlify(command_str.encode()) # encode() method returns an encoded version of the string.
byte_command = binascii.unhexlify(hex_command) # unhexlify() method returns the binary data represented by the hexadecimal string.

#create a Pygatt BLE adapter
adapter = pygatt.GATTToolBackend() # GATTToolBackend is a Python interface for the gatttool (a deprecated tool from BlueZ) using the BGAPI backend from pygattlib.

try:
    #start the adapter
    adapter.start()
    print('Start')
    time.sleep(10)

    #connect to the device
    device = adapter.connect(MAC) # connect() method connects to the device with the specified MAC address.
    print('Connected')
    time.sleep(10)

    #send command
    device.char_write(UUID, byte_command) # char_write() method writes the value of the specified characteristic.

    #receive response
    response = device.char_read(UUID) # char_read() method reads the value of the specified characteristic.
    print(response)

finally:
    #stop the adapter session
    adapter.stop()
    print('Stop')
    time.sleep(10)
