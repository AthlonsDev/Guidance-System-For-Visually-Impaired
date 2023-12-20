import board
import busio
import adafruit_drv2605
import time
i2c = busio.I2C(board.GP3, board.GP2)
drv = adafruit_drv2605.DRV2605(i2c)
ada = adafruit_drv2605

print("DRV2605 found: ", drv)

slot_0_effect = drv.sequence[0]

drv.sequence[0] = ada.Effect(83)
drv.sequence[1] = ada.Effect(85)

drv.mode = ada.MODE_REALTIME
def haptic(distance):
    power = convert_distance(distance)
    #print(power)
        # Start real-time playback
    drv.realtime_value = power
    drv.play()
def stop():
    drv.stop()

def convert_distance(distance):
    power = 0
    if distance > 100:
        distance = 100
    
    power = 100 - distance
    

    return power