import os
import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import cv2
#import lcd
from Adafruit_CharLCD import Adafruit_CharLCD


def tst(strs):
    lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=6, d6=5, d7=11,
                       cols=16, lines=2)
    lcd.clear()
    lcd.message('    [8 team]\n' + 'Human Found : ' + strs)


def lcd_print():
    lcd.lcd_init()
    lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    lcd.lcd_string("Found", 2)
    #lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
    #lcd.lcd_string(strs, 2)
    #lcd.GPIO.cleanup()

def human_count(path):
    imagePath = '/home/pi/pj/pic/' + path
    cascPath = 'yosi.xml'
    faceCascade = cv2.CascadeClassifier(cascPath)
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    return str(len(faces))
    

def ret_distance():
    GPIO.setmode(GPIO.BOARD)
    TRIG = 16
    ECHO = 18
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG, False)
    
    time.sleep(2)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
            pulse_start = time.time()

    while GPIO.input(ECHO)==1:
            pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance, 2)
    GPIO.cleanup()
    if (distance > 1000) != True:
        return distance

def capture():
    with PiCamera() as c:
        c.start_preview()
        time.sleep(1)
        c.capture("/home/pi/pj/pic/" + str(int(time.time())) + ".jpg")
        c.stop_preview()


if __name__ == '__main__':
    a = human_count('abba.png')
    print(a)
    tst(a)

"""
while True:
    retd = ret_distance()
    if (retd < 80) != True:
        print("ok",retd)
        capture()
    else:
        print("nop", retd)
"""
