import distance_sensor as ds
import haptic_feedback as hf
import time
import board
import digitalio
import busio
import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_ble.services.nordic import UARTService

#ble = adafruit_ble.BLERadio()
uart = UARTService()
ble.start_advertising(advertisement)
#uart = busio.UART(board.GP0, board.GP1, baudrate=115200) # board.TX and board.RX are the pins on the board that are connected to the sensor


while True:
    distance = int(ds.get_distance())
    #uart.write(b"hello")
    print("\n", distance)
    if distance<255:
        hf.haptic(distance)
    