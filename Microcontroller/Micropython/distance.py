from machine import Pin
import utime

trigger = Pin(21, Pin.OUT) #obj corresponding to pin 22 on trigger, This will send pulse of current
echo = Pin(22, Pin.IN) #obj corresponding to pin 21 on echo, this will receive reflected pulse


def ultra():
    trigger.low() #ensures it is not active
    utime.sleep_us(2) #pause for 2 mseconds
    #pull trigger pin high 5 mseconds before oulling trigger low
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    #while loop to check echo pin, if no echo is received, then update variable signaloff and store timestamp
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    #while loop to check if echo is received, then store current timestamp to signalon
    while echo.value() == 1:
        signalon = utime.ticks_us()
    #timepassed will store total time taken for the pulse ti leave the sensor, hit the object and return as echo
    timepassed = signalon - signaloff
    
    #distance stores the result of equation. journey(timepassed) times the speed of sound(323,2 m/s) divided by 2
    distance = (timepassed * 0.0343) / 2

    #round the distance to integer value
    distance = round(distance)
    
    #print("the distance from object is ", distance, "cm")
    print(distance)
    return distance
    
while True:
    ultra()
    utime.sleep(1)
    