# Submodule for controling devices like LEDs, Sockets, etc...
import subprocess
import RPi.GPIO as GPIO

def _CtrlLed(device=None, on=True):
    """
    Controll the LEDs on the device board

    Input
    -----
    device, str
        LED name (default=None)
    on, bool
        LED status
    """

    if device == None:
        raise ValueError('Select a device!')

    if device =='LED_socket_A':
        if on:
            GPIO.output(ledPin_Socket_A, GPIO.HIGH)
        else:
            GPIO.output(ledPin_Socket_A, GPIO.LOW)
    elif device =='LED_socket_B':
        if on:
            GPIO.output(ledPin_Socket_B, GPIO.HIGH)
        else:
            GPIO.output(ledPin_Socket_B, GPIO.LOW)
    elif device == 'LED_rast':
        if on:
            GPIO.output(ledPin_Rest, GPIO.HIGH)
        else:
            GPIO.output(ledPin_Rest, GPIO.LOW)
    elif device == 'LED_heating':
        pass
    elif device == 'LED_end':
        if on:
            GPIO.output(ledPin_End, GPIO.HIGH)
        else:
            GPIO.output(ledPin_End, GPIO.LOW)

    return

def _RemoteControlSocket(socket='A', on=True):
    """
    Switches remote socket on and off by transmitting a 344MHz Signal

    Input
    -----
    socket, str
        'A' or 'B' (add further sockets if required)
    on, bool
        if True switch socket on, if False switch socket off


    Returns
    -------
    A_status, bool
        status of socket A
    B_status, bool
        status of socket B

    """
    # Set status to False
    A_status = False
    B_status = False

    # Switch on/off sockets
    if socket == 'A':
        if on:
            cmd = 'python3 send_433.py -p 310 -t 0 17745'
            A_status = True
        else:
            cmd = 'python3 send_433.py -p 310 -t 0 17748'
            A_status = False

    elif socket == 'B':
        if on:
            cmd = 'python3 send_433.py -p 310 -t 0 17745'
            B_status = True
        else:
            cmd = 'python3 send_433.py -p 310 -t 0 17748'
            B_status = False

    # Open subprocess and execute command
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    # Set LED status
    socket_name = 'socket_' + socket
    _CtrlLed(device=socket_name, on=on)

    # Print to LOG
    print('Socket: ', socket, ' Power: ', on)

    return A_status, B_status

def _LCD(lcd, str1='', str2=''):
    """
    Print statement on LCD

    Input
    -----
    str_1, str
        first line string
    str_2, str
        second line string
    """

    lcd.clear()
    lcd.setCursor(0, 0)  # set cursor position
    lcd.message(str1 + '\n')  # display CPU temperature
    lcd.message(str2)  # display the time
    # sleep(1)

    return