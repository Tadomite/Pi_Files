from Shifter import Bug
import RPi.GPIO as GPIO
bug = Bug()
def switchPin(pin):
    state = GPIO.input(pin)
    print("on/off: "+ str(state))
    if state:
        bug.start()
    else:
        bug.stop()
def switchWrap(pin):
    bug.isWrapOn = not bug.isWrapOn
    print("wrap: "+ str(bug.isWrapOn))
def switchSpeed(pin):
    if GPIO.input(pin):
        bug.timeStep = bug.timeStep/3
    else:
        bug.timeStep = bug.timeStep*3
    print("speed: "+ str(bug.timeStep) )
GPIO.setmode(GPIO.BCM)
s1,s2,s3 = 4,17,27
GPIO.setup(s1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s3,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(channel = s1, edge= GPIO.BOTH,callback=switchPin,bouncetime= 100)
GPIO.add_event_detect(channel = s2, edge= GPIO.RISING,callback=switchWrap,bouncetime= 100)
GPIO.add_event_detect(channel = s3, edge= GPIO.BOTH,callback=switchSpeed,bouncetime= 100)


                
try:
     while(True):
         pass
except:
    GPIO.cleanup()   
        