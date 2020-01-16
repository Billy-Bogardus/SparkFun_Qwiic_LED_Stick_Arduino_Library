
import os
import time

LED_Stick_Address = 0x23


COMMAND_CHANGE_ADDRESS = 0xC7
COMMAND_CHANGE_LED_LENGTH = 0x70
COMMAND_WRITE_SINGLE_LED_COLOR = 0x71
COMMAND_WRITE_ALL_LED_COLOR = 0x72
COMMAND_WRITE_RED_ARRAY = 0x73
COMMAND_WRITE_GREEN_ARRAY = 0x74
COMMAND_WRITE_BLUE_ARRAY = 0x75
COMMAND_WRITE_SINGLE_LED_BRIGHTNESS = 0x76
COMMAND_WRITE_ALL_LED_BRIGHTNESS = 0x77
COMMAND_WRITE_ALL_LED_OFF = 0x78


try:
    from Adafruit_GPIO.I2C import Device
    i2c=Device(LED_Stick_Address, 1)
except:
    print("I2C Module Failed")

def setLEDColor( red, green, blue, number=0):
    #all LEDs the same color
    if(type(red)  is int and type(green) is int and type(blue) is int and number == 0):
        data = [red, green, blue]
        print(data)
        i2c.writeList(COMMAND_WRITE_ALL_LED_COLOR,data)
    #set color of individual LED
    elif(type(red)  is int and type(green) is int and type(blue) is int and type(number) is int ):
        data = [number, red, green, blue]
        print(data)
        i2c.writeList(COMMAND_WRITE_SINGLE_LED_COLOR, data)
    #set colors of LED's to individual Colors
    elif(type(red)  is list and type(green) is list and type(blue) is list):
        print("Independent")
        #write Red
        WriteColorArray(COMMAND_WRITE_RED_ARRAY,red)
        print("g")
        #Write Green
        WriteColorArray(COMMAND_WRITE_GREEN_ARRAY,green)
        print("b")
        #Write Blue
        WriteColorArray(COMMAND_WRITE_BLUE_ARRAY,blue)
    else:
        print("Bad Arguments")

def WriteColorArray(command, array):
    length = len(array)+1
    n=0
    arrLen = (length) % 12
    for n in range(length / 12) :
        sliver = slice(n*12,n*12+11)
        data = [12, n*12] + array[sliver] + [12]
        print("12 - "+str(data) )
        i2c.writeList(command, data)
    n = length / 12
    b = 1
    if(n == 0 ):
        b=0
    if ( arrLen > 0 ):
        sliver = slice(n*12-1*b,len(array))
        data = [arrLen, n*12] + array[sliver] + [arrLen]
        print(" > 0 "+str(data) )
        i2c.writeList(command, data)

def blink():
    while(1):
        setLEDColor(0,0,0)
        time.sleep(0.5)
        setLEDColor(30,30,30,2)
        time.sleep(0.5)

def blinkRainbow():
    while(1):
        setLEDColor(0,0,0)
        time.sleep(0.5)
        setLEDColor(
            range(0,30,3),
            ([0] *10) ,
            ([0]* 10) ) 
            #  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 12, 13, 14
        time.sleep(0.5)
def holdgarbage():
        setLEDColor(
            [  0, 30,  0],
            [  0,  0, 30],
            [ 30,  0,  0])
        setLEDColor(
            [  0, 30,  0, 10, 30, 40, 30,  0,  0, 30, 10, 30,  3],
            [  0,  0, 30,  0,  0, 30, 30,  0,  0, 30, 10, 30,  3],
            [ 30,  0,  0, 30, 10, 30, 30,  0,  0, 30, 10, 30,  3])
            #  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 12, 13, 14
        setLEDColor(
            [0] *10,
            range(0,30,3),
            [0]* 10)
            #  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 12, 13, 14
        time.sleep(0.5)
        setLEDColor(
            [0] *10,
            [0]* 10,
            range(0,30,3))
            #  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 12, 13, 14
        time.sleep(0.5)


def allOn():
    setLEDColor(255,255,255)

blinkRainbow()

#allOn()

blink()
