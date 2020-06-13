import RPi.GPIO as GPIO
import time

LED = 11 # pin11

print(" ******** LED Blinking using Raspberry Pi 3 ********* ")
print(" **** Designed by www.TheEngineeringProjects.com **** ")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # We are accessing GPIOs according to their physical location
GPIO.setup(LED, GPIO.OUT) # We have set our LED pin mode to output
GPIO.output(LED, GPIO.LOW) # When it will start then LED will be OFF

while True: #Compiler will keep on executing this loop (infinite loop

    GPIO.output(LED, GPIO.HIGH) # led on
    time.sleep(2) #delay
    GPIO.output(LED, GPIO.LOW) # led off
    time.sleep(2)
