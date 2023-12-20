import board
import busio
import adafruit_drv2605
import time
i2c = busio.I2C(board.GP3, board.GP2)
drv = adafruit_drv2605.DRV2605(i2c)
ada = adafruit_drv2605

slot_0_effect = drv.sequence[0]

drv.sequence[0] = ada.Effect(83)
drv.sequence[1] = ada.Effect(85)

while True:
    drv.play()  # play the effect
    time.sleep(0.5)  # for 0.5 seconds
    drv.stop()  # and then stop (if it's still running)