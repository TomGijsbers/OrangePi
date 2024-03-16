import time
from smbus2 import SMBus, i2c_msg
from bmp280 import BMP280
import paho.mqtt.client as mqtt

# Aanmaken van een I2C bus object voor beide sensoren
bus = SMBus(0)

# Sensoradressen
address_bh1750 = 0x23  # I2C-adres van BH1750
address_bmp280 = 0x77  # I2C-adres van BMP280

# BH1750 initialiseren
def setup_bh1750(bus, address):
    bus.write_byte(address, 0x10)  # 1lx resolutiemodus, zie datasheet

# Lichtniveau uitlezen van BH1750
def get_light_level(bus, address):
    write = i2c_msg.write(address, [0x10])  # Continue meting op 1lx resolutie
    read = i2c_msg.read(address, 2)
    bus.i2c_rdwr(write, read)
    bytes_read = list(read)
    return (((bytes_read[0] & 3) << 8) + bytes_read[1]) / 1.2

# BMP280 initialiseren
bmp280 = BMP280(i2c_addr=address_bmp280, i2c_dev=bus)
interval = 15  # Meetperiode in seconden

# MQTT instellingen
MQTT_HOST = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 120
MQTT_TOPIC = "channels/2463041/publish"
MQTT_CLIENT_ID = "BxQIESYuEAscMDYgIC8jNig"
MQTT_USER = "BxQIESYuEAscMDYgIC8jNig"
MQTT_PWD = "B0Lmy0qD0/dcSerkI3L3U7eY"

# Callback-functie voor als er een connectie gemaakt is met de MQTT server
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Succesvol verbonden met resultaatcode " + str(rc))
    else:
        print("Slechte verbinding met resultaatcode " + str(rc))

# Callback-functie voor als de verbinding met de MQTT server verbroken wordt
def on_disconnect(client, userdata, flags, rc=0):
    print("Verbinding verbroken met resultaatcode " + str(rc))

# Callback-functie voor als er een bericht ontvangen is
def on_message(client, userdata, msg):
    print("Bericht ontvangen op topic: " + msg.topic + "; bericht: " + str(msg.payload))

# MQTT-client aanmaken en instellen
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, MQTT_CLIENT_ID)
client.username_pw_set(MQTT_USER, MQTT_PWD)

# Verbind de callback-functies aan de MQTT-client
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Probeer verbinding te maken met de MQTT server
print("Proberen te verbinden met %s" % MQTT_HOST)
client.connect(MQTT_HOST, MQTT_PORT)
client.loop_start()

# BH1750 klaarzetten voor metingen
setup_bh1750(bus, address_bh1750)  

# Begin met een oneindige lus om meetgegevens te verzamelen en te versturen
while True:
    # Verzamel data van BMP280
    bmp280_temperature = round(bmp280.get_temperature(), 2)
    bmp280_pressure = round(bmp280.get_pressure(), 2)

    # Verzamel lichtniveau van BH1750
    light_level = round(get_light_level(bus, address_bh1750), 2)

    # Print de verzamelde gegevens
    print("Temperatuur: %4.1f°C, Druk: %4.1fhPa, Licht: %4.1fLux" % (bmp280_temperature, bmp280_pressure, light_level))

    # Creëer de MQTT berichtstructuur met de verzamelde gegevens
    MQTT_DATA = "field1={}&field2={}&field3={}&status=MQTTPUBLISH".format(
        bmp280_temperature, bmp280_pressure, light_level,
    )
    print(MQTT_DATA)

    # Probeer het MQTT bericht te publiceren, verbind opnieuw bij een fout
    try:
        client.publish(topic=MQTT_TOPIC, payload=MQTT_DATA, qos=0, retain=False)
    except OSError:
        client.reconnect()

    # Wacht de ingestelde intervalperiode voordat de volgende meting plaatsvindt
    time.sleep(interval)


