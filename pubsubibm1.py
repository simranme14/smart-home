import RPi.GPIO as GPIO
import dht11
import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import json, ast
#Provide your IBM Watson Device Credentials
organization = "0qhs3o"
deviceType = "CRMA"
deviceId = "403421433"
authMethod = "token"
authToken = "aleem789"

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
# read data using pin 12
SensorInstance = dht11.DHT11(pin = 12)


# Initialize the device client.
T=0
H=0

def myCommandCallback(cmd):
        #print("Command received: %s" % cmd.data)
        r =  cmd.data
        k = ast.literal_eval(json.dumps(r))
        l = k['command']
        print(l)
        if l=="Aleem on":
                print ("hi")
                GPIO.output(11,GPIO.HIGH)
                
        elif l== "Aleem of":
                print ("hello")
                GPIO.output(11,GPIO.LOW)
        elif l== "Deeksha on":
                print ("hello1")
                GPIO.output(13,GPIO.HIGH)
        elif l== "Deeksha of":
                print ("hello2")
                GPIO.output(13,GPIO.LOW)
         
       
     

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        #Get Sensor Data from DHT11
        SensorData = SensorInstance.read()
        if SensorData.is_valid():
        #if True:
            T = SensorData.temperature
            H = SensorData.humidity
        else:
            print ("SensorData Invalid")
        #Send Temperature & Humidity to IBM Watson
        data = { 'Temperature' : T, 'Humidity': H }
        #print data
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % T, "Humidity = %s %%" % H, "to IBM Watson")

        success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(1)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
