import RPi.GPIO as GPIO
import time
import random
class Shifter:
    def __init__(self,dataPin, latchPin,clockPin):
        self.dataPin = dataPin
        self.latchPin = latchPin
        self.clockPin = clockPin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(dataPin, GPIO.OUT)
        GPIO.setup(latchPin, GPIO.OUT, initial=0)  # start latch & clock low
        GPIO.setup(clockPin, GPIO.OUT, initial=0)
    def ping(self):
      try:
        for i in range(8):
         GPIO.output(self.dataPin, self.pattern & (1<<i))
         GPIO.output(self.clockPin,1) 	    # ping the clock pin to shift register data
         time.sleep(0)
         GPIO.output(self.clockPin,0)
        GPIO.output(self.latchPin, 1)        # ping the latch pin to send register to output
        time.sleep(0)
        GPIO.output(self.latchPin, 0)
      except:
        GPIO.cleanup()
    def shiftByte(self,pattern):
        self.pattern = pattern
        self.ping()
    
class Bug:
    def __init__(self, timeStep = 0.1, x = 3, isWrapOn = False):
        self.timeStep = timeStep
        self.x = x
        self.isWrapOn = isWrapOn
        self.__shifter = Shifter(23,24,25)
        self.start()
    def start(self):
        self.__active = True
        lastTime = time.time()
        try:
         while(self.__active):
            if time.time()-lastTime > self.timeStep:
                if self.isWrapOn:
                 self.x += random.choice({-1,1})
                 self.x = (self.x+8)%8
                elif self.x == 0:
                    self.x +=1
                elif self.x == 7:
                    self.x -=1
                self.__shifter.shiftByte(1<<(self.x))
        except:
            GPIO.cleanup()
    def stop(self):
        self.__active = False
        self.__shifter.shiftByte(0)
   
    