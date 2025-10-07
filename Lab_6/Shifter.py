import RPi.GPIO as GPIO
import time
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

   
    