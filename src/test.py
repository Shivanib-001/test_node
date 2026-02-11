import sys
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

while True:
    input_data = sys.stdin.read()

    if input_data=='10':
        print("led 1 - off")
        GPIO.output(18,GPIO.LOW)
        
    if input_data=='11':
        print("led 1 - on")
        GPIO.output(18,GPIO.HIGH)
    if input_data=='20':
        print("led 2 - off")
        GPIO.output(18,GPIO.LOW)
        
    if input_data=='21':
        print("led 2 - on")
        GPIO.output(23,GPIO.HIGH)

    

import requests
import time
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
# The URL of your Node.js API
API_URL = "http://localhost:5000/api/led-control"

# Track how many entries we have already processed
processed_count = 0

print("Python Monitor Started... Waiting for signals.")
prev_data=''
while True:
    try:
        # 1. Fetch the data from your Node.js server
        response = requests.get(API_URL)

        if response.status_code == 200:
            # 2. Split the response into individual signal lines
            # .strip() removes empty lines at the end
            lines = response.text.strip().split('\n')

            input_data = lines[0]
            if input_data!=prev_data:   

                if input_data=='10':
                    print("led 1 - off")
                    GPIO.output(18,GPIO.LOW)
                    
                if input_data=='11':
                    print("led 1 - on")
                    GPIO.output(18,GPIO.HIGH)
                if input_data=='20':
                    print("led 2 - off")
                    GPIO.output(18,GPIO.LOW)
                    
                if input_data=='21':
                    print("led 2 - on")
                    GPIO.output(23,GPIO.HIGH)
                prev_data=input_data




    except Exception as e:
        print(f"Error connecting to server: {e}")

    # 4. Wait a short moment before checking again (prevents crashing your PC)
    

