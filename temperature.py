import RPi.GPIO as GPIO
import dht11
import time


# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

# read data using pin 12
SensorInstance = dht11.DHT11(pin = 12)


# Initialize the device client.
T=0
H=0

while True:
    #Get Sensor Data from DHT11
        SensorData = SensorInstance.read()
        if SensorData.is_valid():
                T = SensorData.temperature
                H = SensorData.humidity
        else:
                print ("SensorData Invalid")
        #Send Temperature & Humidity to IBM Watson
        data = { 'Temperature' : T, 'Humidity': H }
        print(data)
