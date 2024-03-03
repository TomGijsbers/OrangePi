import time
import wiringpi

# SETUP
print("Start") 
# R=1K
pinSwitch = 1
wiringpi.wiringPiSetup() 
wiringpi.pinMode(pinSwitch, 0)   

# Infinite loop
while True:
    if(wiringpi.digitalRead(pinSwitch) == 1): #input is active low
        print("Light")
        time.sleep(0.5) #anti bouncing
    else:
        print("Dark")
        time.sleep(0.5) #anti bouncing
     
