import time
import board
import adafruit_dht
from rpi_lcd import LCD
import RPi.GPIO as GPIO 
import requests
#setting up the sensor on GPIO4
dhtDevice = adafruit_dht.DHT11(board.D4)
lcd = LCD()
url= "https://api.thingspeak.com/update"
# Dictionary with the wire key and dummy in
queries = {"api_key": "RJM2YTZGVD6YGHZH", "field1": None, "field2": None}
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
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
                    Thingspeak(temperature, humidity)
                    Fan(temperature)
                    time.sleep(2.0)
            except RuntimeError:
                # If it encounters a runtime error it ignores it
                pass
    except KeyboardInterrupt:
        # If you stop the program with ctrl + c it clears the screen
        lcd.clear()
        GPIO.output(17, False)

def Thingspeak(temp, humi):
    # Assignes the right fields with temperature and humidity
    queries["field1"] = temp
    queries["field2"] = humi
    # Sends the temperature and humidity data to thingspeak
    requests.get(url, params=queries)

def Fan(temp):
    if temp > 27:
        GPIO.output(17, True)
    else:
        GPIO.output(17, False)
    
Main()