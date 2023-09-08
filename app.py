import RPi.GPIO as GPIO
import requests
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TOKEN = "BBFF-yRMjBJE1YOq6AFWKOg2UxHc1hC4Jsr"
DEVICE_LABEL = "Project"
LED_RED = 23
LED_GREEN = 24
BUZZER = 27
PIR = 22

PIR_STATUS = False

def kirim_data(payload):
    print(payload)
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    print(req.status_code, req.json())

    if status >= 400:
        print("Error")
        return False
    print("berhasil")
    return True

GPIO.setup(LED_RED, GPIO.OUT)
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUZZER, GPIO.OUT)

while True:
    if GPIO.input(PIR):
        print("Ada Orang")
        GPIO.output(LED_RED, GPIO.HIGH)
        GPIO.output(LED_GREEN, GPIO.LOW)
        GPIO.output(BUZZER, GPIO.HIGH)
        PIR_STATUS = True
    else:
        print("Aman")
        GPIO.output(LED_RED, GPIO.LOW)
        GPIO.output(LED_GREEN, GPIO.HIGH)
        GPIO.output(BUZZER, GPIO.LOW)
        PIR_STATUS = False
    payload = {"kondisi": int(PIR_STATUS)}
    kirim_data(payload)

    time.sleep(1)