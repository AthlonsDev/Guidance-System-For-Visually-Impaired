import board
import time

import adafruit_hcsr04

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP22, echo_pin=board.GP21)

def get_distance():
    distance = 0
    while True:
        try:
            #print((sonar.distance,))
            distance = (sonar.distance)
        except RuntimeError:
            #print("Retrying...")
            pass
        time.sleep(0.1)
        return distance
        