import time
import wiringpi
import sys

# def blink(_pin):
    # wiringpi.digitalWrite(_pin, 1)    # Write 1 ( HIGH ) to pin
    # time.sleep(0.5)
    # wiringpi.digitalWrite(_pin, 0)    # Write 1 ( HIGH ) to pin
    # time.sleep(0.5)
    # wiringpi.digitalWrite(_pin, 1)    # Write 1 ( HIGH ) to pin
    # time.sleep(0.5)
    # wiringpi.digitalWrite(_pin, 0)    # Write 1 ( HIGH ) to pin
    # time.sleep(0.5)

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



#  Practice 2

# pins = [pin,pin1,pin2,pin3]

# wiringpi.digitalWrite(pin, 1)
# wiringpi.digitalWrite(pin1, 1)
# wiringpi.digitalWrite(pin2, 1)
# wiringpi.digitalWrite(pin3, 1)
# time.sleep(0.1)
# wiringpi.digitalWrite(pin,0 )
# wiringpi.digitalWrite(pin1, 0)
# wiringpi.digitalWrite(pin2, 0)
# wiringpi.digitalWrite(pin3, 0)

#  Practice 4
# pins = [pin,pin1,pin2,pin3,pin3,pin2,pin1,pin]

# for i in pins:
#     wiringpi.digitalWrite(i,1)
#     time.sleep(0.1)
#     wiringpi.digitalWrite(i, 0) 


# Practice 5
# def control_leds(pins, state):
#     for pin in pins:
#         wiringpi.digitalWrite(pin, state)  # state: 1 for HIGH, 0 for LOW

# # Define your pin groups
# group1 = [pin, pin2]
# group2 = [pin1, pin3]

# # Control LEDs
# control_leds(group1, 1)  # Turn on group 1
# time.sleep(0.5)
# control_leds(group1, 0)  # Turn off group 1
# time.sleep(0.5)

# control_leds(group2, 1)  # Turn on group 2
# time.sleep(0.5)
# control_leds(group2, 0)  # Turn off group 2
# time.sleep(0.5)

# Motor
pins = [pin,pin1,pin2,pin3,pin,pin1,pin2,pin3,pin,pin1,pin2,pin3,pin,pin1,pin2,pin3,]

for i in pins:
    wiringpi.digitalWrite(i,1)
    time.sleep(0.5)
    wiringpi.digitalWrite(i, 0) 

#cleanup
print("Done")

