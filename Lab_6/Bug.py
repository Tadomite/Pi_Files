import Bug
import RPi.GPIO as GPIO
bug = Bug()
GPIO.setmode(GPIO.BCM)
s1,s2,s3 = 4,17,27
GPIO.setup(s1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s3,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
def switchPin(pin):
    if GPIO.input(pin):
        bug.start()
    else:
        bug.stop()
def switchWrap(pin):
    bug.isWrapOn = not bug.isWrapOn
def switchSpeed(pin):
    if GPIO.input(pin):
        bug.timeStep = bug.timeStep/3
    else:
        bug.timeStep = bug.timeStep*3
        
GPIO.add_event_detect(channel = s1, edge= GPIO.BOTH,callback=switchPin,bouncetime= 100)
GPIO.add_event_detect(channel = s2, edge= GPIO.RISING,callback=switchWrap,bouncetime= 100)
GPIO.add_event_detect(channel = s3, edge= GPIO.BOTH,callback=switchSpeed,bouncetime= 100)
                
    
        