import time
import RPi.GPIO as GPIO
import math
pins = [4,17,27,22,10,9,11,5,6,13]
GPIO.setmode(GPIO.BCM)
pwm = []
for i in pins:
    GPIO.setup(i,GPIO.OUT,initial=1)
    nPwm = GPIO.PWM(i,500)
    nPwm.start(0.0)
    pwm.append(nPwm)
try:
 while(1):
    for i,j in enumerate(pwm):
        j.ChangeDutyCycle(50+25*math.sin(2*3.14*.2*time.time()+i*3.14/11))
except:
 GPIO.cleanup()
    