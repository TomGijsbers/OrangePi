import time
import wiringpi
import sys

def blink(_pin):
    wiringpi.digitalWrite(_pin, 1)    # Write 1 ( HIGH ) to pin
    time.sleep(0.5)
    wiringpi.digitalWrite(_pin, 0)    # Write 1 ( HIGH ) to pin
    time.sleep(0.5)
    wiringpi.digitalWrite(_pin, 1)    # Write 1 ( HIGH ) to pin
    time.sleep(0.5)
    wiringpi.digitalWrite(_pin, 0)    # Write 1 ( HIGH ) to pin
    time.sleep(0.5)

#SETUP
print("Start")
pin = 2
pin1 = 3
pin2 = 4
pin3 = 6
wiringpi.wiringPiSetup() 
wiringpi.pinMode(pin, 1)            # Set pin to mode 1 ( OUTPUT )
wiringpi.pinMode(pin1, 1)            # Set pin to mode 1 ( OUTPUT )
wiringpi.pinMode(pin2, 1)            # Set pin to mode 1 ( OUTPUT )
wiringpi.pinMode(pin3, 1)            # Set pin to mode 1 ( OUTPUT )

# wiringpi.digitalWrite(pin, 1)    # Write 1 ( HIGH ) to pin
# time.sleep(0.5)
# wiringpi.digitalWrite(pin, 0)    # Write 1 ( HIGH ) to pin
# time.sleep(0.5)
# wiringpi.digitalWrite(pin1, 1)    # Write 1 ( HIGH ) to pin
# time.sleep(0.5)
# wiringpi.digitalWrite(pin1, 0)    # Write 1 ( HIGH ) to pin
# time.sleep(0.5)
# wiringpi.digitalWrite(pin2, 1)    # Write 1 ( HIGH ) to pin
# time.sleep(0.5)
# wiringpi.digitalWrite(pin2, 0)    # Write 1 ( HIGH ) to pin
# time.sleep(0.5)
# wiringpi.digitalWrite(pin3, 1)    # Write 1 ( HIGH ) to pin
# time.sleep(0.5)
# wiringpi.digitalWrite(pin3, 0)    # Write 1 ( HIGH ) to pin
# time.sleep(0.5)


wiringpi.digitalWrite(pin, 1)    # Write 1 ( HIGH ) to pin
wiringpi.digitalWrite(pin2, 1)    # Write 1 ( HIGH ) to pin
time.sleep(0.5)
wiringpi.digitalWrite(pin, 0)    # Write 1 ( HIGH ) to pin
wiringpi.digitalWrite(pin2, 0)  
time.sleep(0.5)
wiringpi.digitalWrite(pin1, 1)    # Write 1 ( HIGH ) to pin
wiringpi.digitalWrite(pin3, 1) 
time.sleep(0.5)
wiringpi.digitalWrite(pin1, 0)    # Write 1 ( HIGH ) to pin
wiringpi.digitalWrite(pin3, 0) 
#cleanup
print("Done")

