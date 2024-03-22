import wiringpi
import time
 
def ActivateADC ():
    wiringpi.digitalWrite(pin_CS_adc, 0) # Actived ADC using CS
    time.sleep(0.000005)
def DeactivateADC():
    wiringpi.digitalWrite(pin_CS_adc, 1) # Deactived ADC using CS
    time.sleep(0.000005)
def readadc(adcnum):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    revlen, recvData = wiringpi.wiringPiSPIDataRW(1, bytes([1,(8+adcnum)<<4,0]))
    time.sleep(0.000005)
    adcout = ((recvData[1]&3) << 8) + recvData[2]
    return adcout
def blink(_pin):
    wiringpi.digitalWrite(_pin, 1)    # Write 1 ( HIGH ) to pin
    time.sleep(0.5)
    wiringpi.digitalWrite(_pin, 0)    # Write 1 ( HIGH ) to pin
    time.sleep(0.5)
#Setup
    #PWM
pinpwm = 2
pinControl = 3
pin_CS_adc = 16 #We will use w16 as CE, not the default pin w15!
wiringpi.wiringPiSetup()
wiringpi.pinMode(pin_CS_adc, 1) # Set ce to mode 1 ( OUTPUT )
wiringpi.wiringPiSPISetupMode(1, 0, 500000, 0) #(channel, port, speed, mode)
 
wiringpi.softPwmCreate(pinpwm,0,1023)
 
wiringpi.softPwmWrite(pinpwm,0)
 
wiringpi.pinMode(pinControl, 1)            # Set pin to mode 1 ( OUTPUT )
 
 
#RGB LED
pinRed = 4
pinGreen = 6
pinBlue = 9
 
wiringpi.pinMode(pinRed, 1)            # Set pin to mode 1 ( OUTPUT )
wiringpi.pinMode(pinGreen, 1)            # Set pin to mode 1 ( OUTPUT )
wiringpi.pinMode(pinBlue, 1)            # Set pin to mode 1 ( OUTPUT )
 
#Ultrasone
pinTrigger = 0
pinEcho = 1
 
wiringpi.pinMode(pinEcho, 0)    # Set pin to mode 0 ( INPUT )
wiringpi.pinMode(pinTrigger, 1)        # Set pin to mode 1 ( OUTPUT )
 
 
 
 
#Main
try:
    while True:
        #ADC
        ActivateADC()
        tmp0 = readadc(0) # read channel 0
        DeactivateADC()
        print ("input0:",tmp0)
        #PWM
        wiringpi.softPwmWrite(pinpwm,tmp0)
        if (tmp0 < 500):
            blink(pinControl)
        else:
            wiringpi.digitalWrite(pinControl,0)
        #ultrasone
        wiringpi.digitalWrite(pinTrigger,1)
        time.sleep(0.00001)
        wiringpi.digitalWrite(pinTrigger,0)
        while (wiringpi.digitalRead(pinEcho) == 0):
            signal_high = time.time()
        while (wiringpi.digitalRead(pinEcho) == 1):
            signal_low = time.time()
        timepassed = signal_low - signal_high
        distance = timepassed * 17000
        distance = round(distance, 1)
        print ('Distance:',distance,'cm')
        if (distance < 50):
            wiringpi.digitalWrite(pinGreen,0)
            wiringpi.digitalWrite(pinBlue,0)
            wiringpi.digitalWrite(pinRed,1)
        elif (distance > 50 and distance < 80):
            wiringpi.digitalWrite(pinGreen,1)
            wiringpi.digitalWrite(pinBlue,0)
            wiringpi.digitalWrite(pinRed,0)
        else:
            wiringpi.digitalWrite(pinGreen,0)
            wiringpi.digitalWrite(pinBlue,1)
            wiringpi.digitalWrite(pinRed,0)
        time.sleep(0.2)
        
        
except KeyboardInterrupt:
    DeactivateADC()
    print("\nProgram terminated")