import machine
led = machine.Pin("LED", machine.Pin.OUT)


#modulate the LED with PWM
pwm = machine.PWM(led)
pwm.freq()
pwm.duty()