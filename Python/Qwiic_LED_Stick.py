#!/usr/bin/python3
import os
import time
import _thread

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
            print("smbus not available. Please make sure this Module is installed.")

    def changeLength(self, length):
        self.bus.write_byte_data(self.LED_Stick_Address, self.COMMAND_CHANGE_LED_LENGTH, length)

    def changeAddress(self, newAddress):
        self.bus.write_byte_data(self.LED_Stick_Address, self.COMMAND_CHANGE_ADDRESS, newAddress)
        self.LED_Stick_Address = newAddress
        #Turn LEDs on and off so address can be changed back imeadiatly
        self.allOn()
        self.allOff()



    #Change the brightness of a specific or all LED, while keeping their current color
    #brightness must be a value between 0-31
    #To turn LEDs off but remember their previous color, set brightness to 0
    #LEDS indexed starting at 1
    #number parameter is optional
    def setLEDBrightness(self, brightness, number=0):
        if(brightness > 31):
            return False
        if(number <= 0):
            self.bus.write_byte_data(self.LED_Stick_Address, self.COMMAND_WRITE_ALL_LED_BRIGHTNESS,
                brightness)
            return True
        else:
            self.bus.write_i2c_block_data(self.LED_Stick_Address, self.COMMAND_WRITE_SINGLE_LED_BRIGHTNESS, 
            [
                number,
                brightness
            ])
            return True

    #Write LED Color(s)
    def setLEDColor(self, red, green, blue, number=0):
        #set colors of LED's to individual Colors
        if(type(red)  is list and type(green) is list and type(blue) is list):
            #write Red
            self.WriteColorArray(self.COMMAND_WRITE_RED_ARRAY,red)
            #Write Green
            self.WriteColorArray(self.COMMAND_WRITE_GREEN_ARRAY,green)
            #Write Blue
            self.WriteColorArray( self.COMMAND_WRITE_BLUE_ARRAY,blue)
        #all LEDs the same color
        elif(type(red)  is int and type(green) is int and type(blue) is int and number == 0):
            data = [red, green, blue]
            self.bus.write_i2c_block_data(self.LED_Stick_Address, self.COMMAND_WRITE_ALL_LED_COLOR, data)
        #set color of individual LED
        elif(type(red)  is int and type(green) is int and type(blue) is int and type(number) is int ):
            data = [number, red, green, blue]
            self.bus.write_i2c_block_data(self.LED_Stick_Address, self.COMMAND_WRITE_SINGLE_LED_COLOR, data)
        else:
            print("Bad Arguments")

    #All LEDs on Full Blast
    def allOn(self):
        self.setLEDColor(255,255,255)
    #All LEDs off
    def allOff(self):
        self.bus.write_byte(self.LED_Stick_Address, self.COMMAND_WRITE_ALL_LED_OFF)

    #Write a Collor array
    def WriteColorArray(self, command, array):
        length = len(array)+1
        n=0
        arrLen = (length) % 12
        chunkRange = range( length // 12)
        for n in chunkRange :
            sliver = slice(n*12,n*12+11)
            data = [12, n*12] + array[sliver] + [12]
            
            self.bus.write_i2c_block_data(self.LED_Stick_Address, command, data)
            n = length // 12
            b = 1
        if(n == 0 ):
            b=0
        if ( arrLen > 0 ):
            sliver = slice(n*12-1*b,len(array))
            data = [arrLen, n*12] + array[sliver] + [arrLen]
            
            self.bus.write_i2c_block_data(self.LED_Stick_Address, command, data)

    #Listen to keyboard 
    def stdIOIn(self, TList):
        a = input()
        print(a)
        TList.append(True)

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

#Blinkes the LED's untill the enter key is pressed.
class Qwiic_LED_Blink(Qwiic_LED_Stick):
    #Simple Blink Code with adjustable on and off delay
    def blink(self, timeA = 0.5, timeB = 0.5):
        B_list = []
        _thread.start_new_thread(self.stdIOIn, (B_list,))
        while not B_list:
            self.setLEDColor(0,0,0)
            time.sleep(timeA)
            self.allOn()
            time.sleep(timeB)
    
    #Blink a rainbow TODO find proper color Values
    def blinkRainbow(self, timeA = 0.5, timeB = 0.5):
        B_list = []
        _thread.start_new_thread(self.stdIOIn, (B_list,))
        while not B_list:
            self.setLEDColor(0,0,0,0)
            #       1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 12, 13, 14
            rr = [  0,  0,  0,148, 75,  0,  0,255,255,255,  0]
            rb = [  0,  0,  0,  0,  0,  0,255,255,165, 10,  0]
            rg = [  0,  0,  0,211,130,255,  0,  0,  0,  0,  0]
            time.sleep(timeA)
            self.setLEDColor(rr,rb,rg)
            time.sleep(timeB)


#class tracks a file and blinks as long as the first five letters do not == False
class Qwiic_LED_Blink_File(Qwiic_LED_Stick):
    #Simple Blink Code with adjustable on and off delay
    def blink(self, timeA = 0.5, timeB = 0.5, filename="Python/text"):
        B_list = []
        _thread.start_new_thread(self.monitorFile, (filename, B_list,))
        while not B_list:
            self.setLEDColor(0,0,0)
            time.sleep(timeA)
            self.allOn()
            time.sleep(timeB)
    
    #Blink a rainbow TODO find proper color Values
    def blinkRainbow(self, timeA = 0.5, timeB = 0.5, filename="Python/text"):
        B_list = []
        _thread.start_new_thread(self.monitorFile, (filename, B_list,))
        while not B_list:
            self.setLEDColor(0,0,0,0)
            #       1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 12, 13, 14
            rr = [  0,  0,  0,148, 75,  0,  0,255,255,255,  0]
            rb = [  0,  0,  0,  0,  0,  0,255,255,165, 10,  0]
            rg = [  0,  0,  0,211,130,255,  0,  0,  0,  0,  0]
            time.sleep(timeA)
            self.setLEDColor(rr,rb,rg)
            time.sleep(timeB)
    #This function will be launched in a different thread and will monitor the specified file for a value of False
    def monitorFile(self, filename, TList):
        f = open(filename,"r")
        val = True
        while val:
            text = f.read(5)
            if(text == "False"):
                val = False
            f.seek(0)
        f.close()
        TList.append(True)
    def resetFile(self, filename):
        f = open(filename, "wt")
        f.write("True")
        f.close()

# Test File based Loop
if __name__ == '__main__':
    print("Test Script for Qwiic_LED_Stick module")
    print("Press Enter to exit")
    #initialize module
    bling = Qwiic_LED_Blink_File(1)
    #set brightness to 1 I like my eyeballs
    bling.setLEDBrightness(1)
    #blink LED
    bling.changeLength(10)
    bling.resetFile("Python/text")
    bling.blink()
    #bling.allOn()
    #time.sleep(0.5)
    #bling.allOff()
    #time.sleep(0.5)
    #blink Rainbow
    bling.resetFile("Python/text")
    bling.blinkRainbow()
    bling.resetFile("Python/text")
    bling.allOff()
