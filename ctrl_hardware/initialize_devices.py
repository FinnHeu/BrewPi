# Submodule for initializing the single devices
import time
import os
import glob
import numpy as np
import RPi.GPIO as GPIO
import ctrl_hardware.constants as c
from ctrl_hardware.Adafruit_LCD1602 import Adafruit_CharLCD
from ctrl_hardware.PCF8574 import PCF8574_GPIO
from ctrl_brewing.brewing_process import MeanTemp
from ctrl_hardware.device_ctrl import LCD, RemoteControlSocket



def InitializeGPIOs(lcd):
    '''
    Assign pins
    '''

    ### Start Processes
    LCD(lcd, str1='---> BrewPi <---')
    time.sleep(3)

    ########################################## GPIOS ################################################
    ### Set GPIO pins as global variables
    LCD(lcd, str1='Assigning', str2='GPIOs...')

    ### Set pin numbering and standard levels for LEDs
    GPIO.setmode(GPIO.BOARD) # use physical numbering on GPIOs
    # LED Heizen
    GPIO.setup(c.ledPin_Socket_A, GPIO.OUT) # set the led pin to Output mode
    GPIO.output(c.ledPin_Socket_A, GPIO.LOW) # make standard level of led pin low
    # LED On
    GPIO.setup(c.ledPin_On, GPIO.OUT) # set the led pin to Output mode
    GPIO.output(c.ledPin_On, GPIO.HIGH) # make standard level of led pin low
    # LED Rast
    GPIO.setup(c.ledPin_Rest, GPIO.OUT) # set the led pin to Output mode
    GPIO.output(c.ledPin_Rest, GPIO.LOW) # make standard level of led pin low
    # LED End
    GPIO.setup(c.ledPin_End, GPIO.OUT) # set the led pin to Output mode
    GPIO.output(c.ledPin_End, GPIO.LOW) # make standard level of led pin low

    return

def InitializeThermistors(lcd):
    """
    Initialize thermistors

    Returns
    -------
    device_file, list() list of files pointing to the temperature values
    """
    # Activate temperature sensor
    LCD(lcd, str1='Activating', str2='Thermistors...')

    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    # Locate the thermistors
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')

    device_file = list()
    for i in range(3):
        device_file.append(device_folder[i] + '/w1_slave')

    time.sleep(2)

    return device_file

def InitializeLCD():
    """
    Initialize LCD screen

    Returns
    -------
    lcd,
    """

    PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
    PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.

    # Create PCF8574 GPIO adapter.
    try:
        mcp = PCF8574_GPIO(PCF8574_address)
    except:
        try:
            mcp = PCF8574_GPIO(PCF8574A_address)
        except:
            print ('I2C Address Error !')

    # Create LCD, passing in MCP GPIO adapter.
    lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp)
    mcp.output(3, 1)  # turn on LCD backlight
    lcd.begin(16, 2)  # set number of LCD lines and columns

    return lcd

def InitTests(lcd, device_file, ledPin_Socket_A):
    """"""

    # Start brewing with some test...
    LCD(lcd, str1='Initializing...', str2='Please Wait...')
    time.sleep(3)

    LCD(lcd, str1='Check 433MHz', str2='Watch Cooker!')
    RemoteControlSocket(socket='A', on=True)
    time.sleep(3)
    RemoteControlSocket(socket='A', on=False)
    LCD(lcd, str1='If failed', str2='Press CTRL + C')
    time.sleep(3)

    #RemoteControlSocket(socket='B', on=True)
    #time.sleep(3)
    #RemoteControlSocket(socket='B', on=False)
    #LCD(lcd, str1='If failed', str2='Press CTRL + C')
    #time.sleep(3)

    # check temperature sensors for consistency
    LCD(lcd, str1='Checking', str2='Thermistors...')
    time.sleep(2)

    temp_consistency = False
    while temp_consistency == False:
        # recieve the deviation from the mean temperature
        temp_diff = MeanTemp(device_file, consistency_check=True)
        # check deviation from mean temperature
        if any(t > .5 for t in temp_diff):
            LCD(lcd, str1='Temp:' + str(np.round(temp_diff[0], decimals=2)) + 'C ',
                str2=str(np.round(temp_diff[1], decimals=2)) + 'C ' + str(np.round(temp_diff[2], decimals=2)) + 'C ')
            time.sleep(3)
            LCD(lcd, str1='Thermistors are ',
                 str2='calibrated...')
        else:
            temp_consistency = True

        time.sleep(2)

    LCD(lcd, str1='Thermistors', str2='ready!')
    time.sleep(2)

def Initialize():
    """
    Main function of this submodule: Runs all initialization routines
    """

    lcd = InitializeLCD()

    InitializeGPIOs(lcd)

    device_file = InitializeThermistors(lcd)

    InitTests(lcd, device_file, c.ledPin_Socket_A)

    return lcd, device_file
