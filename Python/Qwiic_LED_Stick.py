#!/usr/bin/python3
import os
import time

#Module for Qwiic_LED_Stick
class Qwiic_LED_Stick:
    def __init__(self, bussAddr, chipAddr = 0x23):

        # Define Constants
        self.LED_Stick_Address = chipAddr
        self.COMMAND_CHANGE_ADDRESS = 0xC7
        self.COMMAND_CHANGE_LED_LENGTH = 0x70
        self.COMMAND_WRITE_SINGLE_LED_COLOR = 0x71
        self.COMMAND_WRITE_ALL_LED_COLOR = 0x72
        self.COMMAND_WRITE_RED_ARRAY = 0x73
        self.COMMAND_WRITE_GREEN_ARRAY = 0x74
        self.COMMAND_WRITE_BLUE_ARRAY = 0x75
        self.COMMAND_WRITE_SINGLE_LED_BRIGHTNESS = 0x76
        self.COMMAND_WRITE_ALL_LED_BRIGHTNESS = 0x77
        self.COMMAND_WRITE_ALL_LED_OFF = 0x78
        try:
            from smbus import SMBus
            self.bus = SMBus(bussAddr)
        except:
            print("smbus not available")

    #Write LED Color(s)
    def setLEDColor(self, red, green, blue, number=0):
        #set colors of LED's to individual Colors
        if(type(red)  is list and type(green) is list and type(blue) is list):
            print("Independent")
            #write Red
            #TODO This function does not imitate the original Progrogram
            self.WriteColorArray(self.COMMAND_WRITE_RED_ARRAY,red)
            #print("g")
            ##Write Green
            self.WriteColorArray(self.COMMAND_WRITE_GREEN_ARRAY,green)
            #print("b")
            ##Write Blue
            self.WriteColorArray( self.COMMAND_WRITE_BLUE_ARRAY,blue)
        #all LEDs the same color
        elif(type(red)  is int and type(green) is int and type(blue) is int and number == 0):
            data = [red, green, blue]
            print(data)
            self.bus.write_i2c_block_data(self.LED_Stick_Address, self.COMMAND_WRITE_ALL_LED_COLOR, data)
        #set color of individual LED
        elif(type(red)  is int and type(green) is int and type(blue) is int and type(number) is int ):
            data = [number, red, green, blue]
            print(data)
            self.bus.write_i2c_block_data(self.LED_Stick_Address, self.COMMAND_WRITE_SINGLE_LED_COLOR, data)
        else:
            print("Bad Arguments")

    #Simple Blink Code
    def blink(self, timeA = 0.5, timeB = 0.5):
        while(1):
            self.setLEDColor(0,0,0)
            time.sleep(timeA)
            self.setLEDColor(30,30,30,2)#TODO add configuration for this code
            time.sleep(timeB)
    
    #Blink a rainbow TODO find proper color Values
    def blinkRainbow(self, timeA = 0.5, timeB = 0.5):
        while(1):
            self.setLEDColor(0,0,0,0)
            #       1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 12, 13, 14
            rr = [148, 75,  0,  0,255,255,255,  0,  0,  0,  0]
            rb = [  0,  0,  0,255,255,127, 10,  0,  0,  0,  0]
            rg = [211,130,255,  0,  0,  0,  0,  0,  0,  0,  0]
            time.sleep(timeA)
            self.setLEDColor(rr,rb,rg)
            time.sleep(timeB)

    #All LEDs on Full Blast
    def allOn(self):
        self.setLEDColor(255,255,255,0)
    #All LEDs off
    def allOff(self):
        self.setLEDColor(0,0,0,0)

    #Write a Collor array
    def WriteColorArray(self, command, array):
        length = len(array)+1
        n=0
        arrLen = (length) % 12
        chunkRange = range( length // 12)
        for n in chunkRange :
            sliver = slice(n*12,n*12+11)
            data = [12, n*12] + array[sliver] + [12]
            print("12 - "+str(data) )
            self.bus.write_i2c_block_data(self.LED_Stick_Address, command, data)
            n = length // 12
            b = 1
        if(n == 0 ):
            b=0
        if ( arrLen > 0 ):
            sliver = slice(n*12-1*b,len(array))
            data = [arrLen, n*12] + array[sliver] + [arrLen]
            print(" > 0 "+str(data) )
            self.bus.write_i2c_block_data(self.LED_Stick_Address, command, data)
    
    #arrays for use latter
    def holdgarbage(self):
            self.setLEDColor(
                [  0, 30,  0],
                [  0,  0, 30],
                [ 30,  0,  0])
            self.setLEDColor(
                [  0, 30,  0, 10, 30, 40, 30,  0,  0, 30, 10, 30,  3],
                [  0,  0, 30,  0,  0, 30, 30,  0,  0, 30, 10, 30,  3],
                [ 30,  0,  0, 30, 10, 30, 30,  0,  0, 30, 10, 30,  3])
                #  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 12, 13, 14
            self.setLEDColor(
                [0] *10,
                range(0,30,3),
                [0]* 10)
                #  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 12, 13, 14
            time.sleep(0.5)
            self.setLEDColor(
                [0] *10,
                [0]* 10,
                range(0,30,3))
                #  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 12, 13, 14
            time.sleep(0.5)


bling = Qwiic_LED_Stick(1)
#bling.blink()
bling.blinkRainbow()

#blinkRainbow()

#allOn()

#blink()
