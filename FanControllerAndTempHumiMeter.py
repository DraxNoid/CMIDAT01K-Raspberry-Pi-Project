import time
import board
import adafruit_dht
from rpi_lcd import LCD
import RPi.GPIO as GPIO 
import requests
import json
#setting up the sensor on GPIO4
dhtDevice = adafruit_dht.DHT11(board.D4)
lcd = LCD()
writeUrl= "https://api.thingspeak.com/update"
writeQueries = {"api_key": "RJM2YTZGVD6YGHZH", "field1": None, "field2": None, "field3": None}
readUrl= "https://api.thingspeak.com/channels/1442136/feeds.json"
readQueries = {"api_key": "IK2UFZMKC5QQ9Y6E", "results": 1}
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(13,GPIO.IN)
FanCounter = 0
TempThreshold = 0
def Main():
    try:
        while True:
            try: 
                # Assigning temperature and humidity data from the sensor
                temperature = dhtDevice.temperature
                humidity = dhtDevice.humidity
                # Printing out the temperature and humidity
                if temperature is not None and humidity is not None:
                    print(f"Temp={temperature:0.1f}C  Humidity={humidity}%")
                    # Showing the temperature and humidity level on the LCD screen
                    lcd.text(f"Temp = {temperature:0.1f}C", 1)
                    lcd.text(f"Humi = {humidity}%", 2)
                    # Calling the thingspeak function and giving it the temperature and humidity
                    ThingspeakWrite(temperature, humidity)
                    Fan(temperature)
                    time.sleep(2.0)
            except RuntimeError:
                # If it encounters a runtime error it ignores it
                pass
    except KeyboardInterrupt:
        # If you stop the program with ctrl + c it clears the screen
        lcd.clear()
        GPIO.output(17, False)

def ThingspeakWrite(temp, humi):
    # Assignes the right fields with temperature, humidity and the amount of time the fan has turned on
    writeQueries["field1"] = temp
    writeQueries["field2"] = humi
    writeQueries["field3"] = FanCounter
    # Sends the temperature and humidity data to thingspeak
    requests.get(writeUrl, params=writeQueries)
def ThingspeakRead():
    global FanCounter
    data = requests.get(readUrl, params=readQueries).json()
    FanCounter = int(data["feeds"][0]["field3"])

def Fan(temp):
    global FanCounter
    if temp > TempThreshold and GPIO.input(17) == False:
        GPIO.output(17, True)
        FanCounter += 1
        print(FanCounter)
    elif temp < TempThreshold:
        GPIO.output(17, False)

ThingspeakRead()
Main()