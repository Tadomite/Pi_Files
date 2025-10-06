import time
import RPi.GPIO as GPIO
import math
pins = [4,17,27,22,10,9,11,5,6,13]
GPIO.setmode(GPIO.BCM)
pwm = []
GPIO.setup(19,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
for i in pins:
    GPIO.setup(i,GPIO.OUT,initial=1)
    nPwm = GPIO.PWM(i,500)
    nPwm.start(0.0)
    pwm.append(nPwm)
sign = 1
def switchSign():
    sign =  sign*-1
try:
 GPIO.add_event_detect(channel = 19, edge= GPIO.RISING,callback=switchSign)
 while(1):
    for i,j in enumerate(pwm):
        j.ChangeDutyCycle(50+50*math.sin(2*3.14*.2*time.time()-sign*i*3.14/11))
except:
 GPIO.cleanup()
    