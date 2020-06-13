import RPi.GPIO as GPIO
import dht11
import time
import datetime
import requests

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin=14)

while True:
    result = instance.read()
    if result.is_valid():
        print("Last valid input: " + str(datetime.datetime.now()))
        print("Temperature: %d C" % result.temperature)
        print("Humidity: %d %%" % result.humidity)
        temp=result.temperature
        hum=result.humidity
        response=requests.get("https://api.thingspeak.com/update?api_key=VHSO3PD33HPJRHBD&field1="+str(temp)+"&field2="+str(hum))
        print(response.status_code)
    time.sleep(1)
