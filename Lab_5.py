import time
import RPi.GPIO as GPIO
import math
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.OUT,initial=1)
pwm = GPIO.PWM(4,500)
pwm.start(0.0)
while(1):
    print(50+100*math.sin(2*3.14*.2*time.time()))
    pwm.ChangeDutyCycle(50+100*math.sin(2*3.14*.2*time.time()))
