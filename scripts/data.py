# Imports
import time
from smbus2 import SMBus, i2c_msg
from bmp280 import BMP280
import paho.mqtt.client as mqtt
import wiringpi

# I2C bus object en sensoradressen
bus = SMBus(0)  # Maak een I2C bus object
address_bh1750 = 0x23  # BH1750 I2C adres
address_bmp280 = 0x77  # BMP280 I2C adres

# MQTT instellingen
MQTT_HOST = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 120
MQTT_TOPIC = "channels/2463041/publish"
MQTT_CLIENT_ID = "BxQIESYuEAscMDYgIC8jNig"
MQTT_USER = "BxQIESYuEAscMDYgIC8jNig"
MQTT_PWD = "B0Lmy0qD0/dcSerkI3L3U7eY"

# GPIO en SPI instellingen
pwm_pin = 2
pin_CS_adc = 16  # Chip select pin voor ADC
wiringpi.wiringPiSetup()
wiringpi.wiringPiSPISetupMode(1, 0, 500000, 0)  # SPI setup
wiringpi.softPwmCreate(pwm_pin, 0, 100)  # Software PWM setup
wiringpi.pinMode(pin_CS_adc, wiringpi.OUTPUT)
wiringpi.pinMode(pwm_pin, wiringpi.OUTPUT)

# Functies voor het instellen en uitlezen van sensoren
def setup_bh1750(bus, address):
    """Initialiseer BH1750 lichtsensor."""
    bus.write_byte(address, 0x10)  # 1lx resolutie mode, zie datasheet

def get_light_level(bus, address):
    """Lees lichtniveau uit BH1750 sensor."""
    write = i2c_msg.write(address, [0x10])  # Continue meting op 1lx resolutie
    read = i2c_msg.read(address, 2)
    bus.i2c_rdwr(write, read)
    bytes_read = list(read)
    return (((bytes_read[0] & 3) << 8) + bytes_read[1]) / 1.2

def ActivateADC():
    """Activeer ADC met Chip Select op LOW."""
    wiringpi.digitalWrite(pin_CS_adc, wiringpi.LOW)
    time.sleep(0.000005)

def DeactivateADC():
    """Deactiveer ADC met Chip Select op HIGH."""
    wiringpi.digitalWrite(pin_CS_adc, wiringpi.HIGH)
    time.sleep(0.000005)

def readadc(adcnum):
    """Lees waarde van ADC."""
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    revlen, recvData = wiringpi.wiringPiSPIDataRW(1, bytes([1, (8 + adcnum) << 4, 0]))
    time.sleep(0.000005)
    adcout = ((recvData[1] & 3) << 8) + recvData[2]
    return int((adcout / 1023.0) * 100)  # Geschaalde waarde van 0 tot 100

# MQTT callback functies
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK with result code " + str(rc))
    else:
        print("Bad connection with result code " + str(rc))

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code " + str(rc))

def on_message(client, userdata, msg):
    print("Received a message on topic: " + msg.topic + "; message: " + msg.payload)

# MQTT client setup
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, MQTT_CLIENT_ID)
client.username_pw_set(MQTT_USER, MQTT_PWD)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# BMP280 setup
bmp280 = BMP280(i2c_addr=address_bmp280, i2c_dev=bus)
interval = 15  # Sampleperiode in seconden

# Hoofduitvoering van het programma
if __name__ == "__main__":
    print("Attempting to connect to %s" % MQTT_HOST)
    client.connect(MQTT_HOST, MQTT_PORT)
    client.loop_start()

    setup_bh1750(bus, address_bh1750)  # Bereid BH1750 voor op metingen

    while True:
        # Meet data van BMP280
        bmp280_temperature = round(bmp280.get_temperature(), 2)
        bmp280_pressure = round(bmp280.get_pressure(), 2)

        # Meet lichtniveau van BH1750
        light_level = round(get_light_level(bus, address_bh1750), 2)

        # Creëer MQTT datastructuur met gemeten waarden
        MQTT_DATA = "field1={}&field2={}&field3={}&status=MQTTPUBLISH".format(
            bmp280_temperature, bmp280_pressure, light_level,
        )

        # Update potentiometer waarde en pas PWM waarde aan
        ActivateADC()
        potmetervalue = readadc(0)  # Lees potentiometer waarde
        DeactivateADC()
        
        # Bereken verschil tussen gewenste en gemeten lux, pas PWM aan
        lux_difference = potmetervalue - light_level
        if abs(lux_difference) <= 10:
            step_size = 2
        else:
            step_size = 10
        if lux_difference > 0:
            pwm_value = min(100, pwm_value + step_size)
        elif lux_difference < 0:
            pwm_value = max(0, pwm_value - step_size)
        wiringpi.softPwmWrite(pwm_pin, pwm_value)

        # Debugging prints
        print(f"Potentiometerwaarde: {potmetervalue}, Lichtniveau: {light_level}, PWM-waarde: {pwm_value}")

        try:
            client.publish(topic=MQTT_TOPIC, payload=MQTT_DATA, qos=0, retain=False)
        except OSError:
            client.reconnect()

        time.sleep(interval)
