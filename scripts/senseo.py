import time
from smbus2 import SMBus, i2c_msg
from bmp280 import BMP280
import paho.mqtt.client as mqtt
import wiringpi




# Create an I2C bus object for both sensors
bus = SMBus(0)

# Sensor addresses
address_bh1750 = 0x23  # BH1750 I2C address
address_bmp280 = 0x77  # BMP280 I2C address

# Setup BH1750
def setup_bh1750(bus, address):
    bus.write_byte(address, 0x10)  # 1lx resolution mode, see datasheet

# Read light level from BH1750
def get_light_level(bus, address):
    write = i2c_msg.write(address, [0x10])  # Continuous measurement at 1lx resolution
    read = i2c_msg.read(address, 2)
    bus.i2c_rdwr(write, read)
    bytes_read = list(read)
    return (((bytes_read[0] & 3) << 8) + bytes_read[1]) / 1.2


# PWN
# ADC activeren met CS (Chip select) op LOW en deactiveren op HIGH.
def ActivateADC ():
   wiringpi.digitalWrite(pin_CS_adc, wiringpi.LOW)
   time.sleep(0.000005)
def DeactivateADC():
   wiringpi.digitalWrite(pin_CS_adc, wiringpi.HIGH) 
   time.sleep(0.000005)
   
# Functie om waarde van de adc te lezen. Adcnum is het kanaal waarvan gelezen wordt.
def readadc(adcnum): 
    if ((adcnum > 7) or (adcnum < 0)): 
        return -1 
    revlen, recvData = wiringpi.wiringPiSPIDataRW(1, bytes([1, (8 + adcnum) << 4, 0]))
    time.sleep(0.000005)
    adcout = ((recvData[1] & 3) << 8) + recvData[2]
    return int((adcout / 1023.0) * 100)  # Scaled value from 0 to 100




# Setup BMP280
bmp280 = BMP280(i2c_addr=address_bmp280, i2c_dev=bus)
interval = 15  # Sample period in seconds

# MQTT settings
MQTT_HOST = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 120
MQTT_TOPIC = "channels/2463041/publish"
MQTT_CLIENT_ID = "BxQIESYuEAscMDYgIC8jNig"
MQTT_USER = "BxQIESYuEAscMDYgIC8jNig"
MQTT_PWD = "B0Lmy0qD0/dcSerkI3L3U7eY"

# Mosquitto MQTT instellingen
MOSQUITTO_HOST = "localhost"
MOSQUITTO_PORT = 1883
MOSQUITTO_TOPIC = "GP/IoT"




# desired_temperature = 25.0  # Gewenste temperatuur in graden Celsius
# desired_pressure = 1013.25  # Gewenste druk in hPa
# desired_brightness = 500.0  # Gewenste helderheid in Lux

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK with result code " + str(rc))
    else:
        print("Bad connection with result code " + str(rc))

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code " + str(rc))

def on_message(client, userdata, msg):
    print("Received a message on topic: " + msg.topic + "; message: " + msg.payload)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, MQTT_CLIENT_ID)
client.username_pw_set(MQTT_USER, MQTT_PWD)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

print("Attempting to connect to %s" % MQTT_HOST)
client.connect(MQTT_HOST, MQTT_PORT)
client.loop_start()

setup_bh1750(bus, address_bh1750)  # Prepare BH1750 for measurements


# Maak een MQTT client voor Mosquitto
# mosquitto_client = mqtt.Client()
# mosquitto_client.connect(MOSQUITTO_HOST, MOSQUITTO_PORT, 60)



pwm_pin =2
# Toewijzen van een pin aan de ADC.
pin_CS_adc = 16  
wiringpi.wiringPiSetup()
 # SPI Setup.
wiringpi.wiringPiSPISetupMode(1, 0, 500000, 0) #(channel, port, speed, mode)
# Initiatie van een softwarematige PWM op pwm_pin met startwaarde 0 en range tot 100.
wiringpi.softPwmCreate(pwm_pin, 0, 100)
wiringpi.pinMode(pin_CS_adc, wiringpi.OUTPUT)
wiringpi.pinMode(pwm_pin, wiringpi.OUTPUT)


pwm_value = 0  # Initialisatie van pwm_value buiten de while-loop


while True:
    # Meet data van BMP280
    bmp280_temperature = round(bmp280.get_temperature(), 2)
    bmp280_pressure = round(bmp280.get_pressure(), 2)

    # Meet lichtniveau van BH1750
    light_level = round(get_light_level(bus, address_bh1750), 2)

    # print("Temperature: %4.1f°C, Pressure: %4.1fhPa, Light: %4.1fLux" % (bmp280_temperature, bmp280_pressure, light_level))

    # Creëer de MQTT data structuur inclusief gemeten
    MQTT_DATA = "field1={}&field2={}&field3={}&status=MQTTPUBLISH".format(
        bmp280_temperature, bmp280_pressure, light_level,
        
    )
    # print(MQTT_DATA)

# Laagste = rood
# Midden = groen
# Hoogste = blauw


    # if (light_level < 50):
    #     wiringpi.digitalWrite(pwm_pin,0)
    # elif (light_level > 50 and light_level < 80):
    #     wiringpi.digitalWrite(pwm_pin,0)
    # else: 
    #     wiringpi.digitalWrite(pwm_pin,1)

    ActivateADC()
    potmetervalue = readadc(0)  # Nu direct van 0 tot 100
    DeactivateADC()
       
       # Waarde van de output herberekenen.
    # pwm_value = int((potmetervalue / 1023.0) * 100)
 
       # PWM waarde aan een LED toekennen.
    # if(pwm_value < 30):
    #     print("PWM value:", pwm_value)
 
    print ("Potentiometer value:", potmetervalue, "PWM value:", pwm_value)

        # Bereken het verschil tussen gewenste lux (potentiometer) en gemeten lux
    # lux_difference = potmetervalue - light_level

    # # Pas de pwm_value aan op basis van het verschil
    # if lux_difference > 0:
    #     pwm_value = min(100, pwm_value + 10)  # Verhoog als het gemeten luxniveau te laag is
    # elif lux_difference < 0:
    #     pwm_value = max(0, pwm_value - 10)  # Verlaag als het gemeten luxniveau te hoog is

    # # Pas de nieuwe PWM-waarde toe op de LED
    # wiringpi.softPwmWrite(pwm_pin, pwm_value)


# Bereken het verschil tussen gewenste lux (potentiometer) en gemeten lux
    lux_difference = potmetervalue - light_level

# Stel een drempel in voor het gebruik van kleine stappen
    small_step_threshold = 10  # De drempelwaarde waarbij we overschakelen naar kleinere stappen

# Kies de stapgrootte op basis van het verschil
    if abs(lux_difference) <= small_step_threshold:
        step_size = 2  # Gebruik een kleine stapgrootte dicht bij het doel
    else:
        step_size = 10  # Gebruik een grotere stapgrootte als het verschil groot is

# Pas de pwm_value aan op basis van het verschil en de stapgrootte
    if lux_difference > 0:
        pwm_value = min(100, pwm_value + step_size)  # Verhoog als het gemeten luxniveau te laag is
    elif lux_difference < 0:
        pwm_value = max(0, pwm_value - step_size)  # Verlaag als het gemeten luxniveau te hoog is

# Pas de nieuwe PWM-waarde toe op de LED
    wiringpi.softPwmWrite(pwm_pin, pwm_value)

    # Print de waarden voor debugging
    print(f"Potentiometerwaarde: {potmetervalue}, Lichtniveau: {light_level}, PWM-waarde: {pwm_value}")


    try:
        client.publish(topic=MQTT_TOPIC, payload=MQTT_DATA, qos=0, retain=False)
    except OSError:
        client.reconnect()
        

    time.sleep(interval)
