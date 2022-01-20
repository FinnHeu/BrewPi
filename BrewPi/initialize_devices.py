# Submodule for initializing the single devices
from .device_ctrl import _LCD, _RemoteControlSocket
import time
import os
import glob
import numpy as np
import RPi.GPIO as GPIO
from .Adafruit_LCD1602 import Adafruit_CharLCD
from .PCF8574 import PCF8574_GPIO
from.brewing_process import _MeanTemp



def _InitializeGPIOs(lcd):
    '''
    Assign pins
    '''

    ### Start Processes
    _LCD(lcd, str1='---> BrewPi <---')
    time.sleep(3)

    ########################################## GPIOS ################################################
    ### Set GPIO pins as global variables
    _LCD(lcd, str1='Assigning', str2='GPIOs...')
    ledPin_Socket_A = 40
    ledPin_On = 37
    ledPin_Rest = 38
    ledPin_End = 22

    ### Set pin numbering and standard levels for LEDs
    GPIO.setmode(GPIO.BOARD) # use physical numbering on GPIOs
    # LED Heizen
    GPIO.setup(ledPin_Socket_A, GPIO.OUT) # set the led pin to Output mode
    GPIO.output(ledPin_Socket_A, GPIO.LOW) # make standard level of led pin low
    # LED On
    GPIO.setup(ledPin_On, GPIO.OUT) # set the led pin to Output mode
    GPIO.output(ledPin_On, GPIO.HIGH) # make standard level of led pin low
    # LED Rast
    GPIO.setup(ledPin_Rest, GPIO.OUT) # set the led pin to Output mode
    GPIO.output(ledPin_Rest, GPIO.LOW) # make standard level of led pin low
    # LED End
    GPIO.setup(ledPin_End, GPIO.OUT) # set the led pin to Output mode
    GPIO.output(ledPin_End, GPIO.LOW) # make standard level of led pin low

    return ledPin_Socket_A, ledPin_Rest, ledPin_On, ledPin_End

def _InitializeThermistors(lcd):
    """
    Initialize thermistors

    Returns
    -------
    device_file, list() list of files pointing to the temperature values
    """
    # Activate temperature sensor
    _LCD(lcd, str1='Activating', str2='Thermistors...')

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

def _InitializeLCD():
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

def _InitTests(lcd, device_file, ledPin_Socket_A):
    """"""

    # Start brewing with some test...
    _LCD(lcd, str1='Initializing...', str2='Please Wait...')
    time.sleep(3)

    _LCD(lcd, str1='Check 433MHz', str2='Watch Cooker!')
    A_status, B_status = _RemoteControlSocket(socket='A', on=True, ledPin_Socket_A)
    time.sleep(3)
    A_status, B_status = _RemoteControlSocket(socket='A', on=False, ledPin_Socket_A)
    _LCD(lcd, str1='If failed', str2='Press CTRL + C')
    time.sleep(3)

    #A_status, B_status = _RemoteControlSocket(socket='B', on=True)
    #time.sleep(3)
    #A_status, B_status = _RemoteControlSocket(socket='B', on=False)
    #_LCD(lcd, str1='If failed', str2='Press CTRL + C')
    #time.sleep(3)

    # check temperature sensors for consistency
    _LCD(lcd, str1='Checking', str2='Thermistors...')
    time.sleep(2)

    temp_consistency = False
    while temp_consistency == False:
        # recieve the deviation from the mean temperature
        temp_diff = _MeanTemp(device_file, consistency_check=True)
        # check deviation from mean temperature
        if any(t > .5 for t in temp_diff):
            _LCD(lcd, str1='Temp:' + str(np.round(temp_diff[0], decimals=2)) + 'C ',
                str2=str(np.round(temp_diff[1], decimals=2)) + 'C ' + str(np.round(temp_diff[2], decimals=2)) + 'C ')
            time.sleep(3)
            _LCD(lcd, str1='Thermistors are ',
                 str2='calibrated...')
        else:
            temp_consistency = True

        time.sleep(2)

    _LCD(lcd, str1='Thermistors', str2='ready!')
    time.sleep(2)

def Initialize():
    """
    Main function of this submodule: Runs all initialization routines
    """

    lcd = _InitializeLCD()

    ledPin_Socket_A, ledPin_Rest, ledPin_On, ledPin_End = _InitializeGPIOs(lcd)

    device_file = _InitializeThermistors(lcd)

    _InitTests(lcd, device_file, ledPin_Socket_A)

    return lcd, device_file, ledPin_Socket_A, ledPin_Rest, ledPin_On, ledPin_End
