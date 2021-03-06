from .device_ctrl import _LCD, _RemoteControlSocket, _CtrlLed
import datetime
import time

def _ReadThermistor(device_file, number=0):
    """
    Read the temperature from a thermistor

    Input
    -----
    number, int
        number of thermistor

    """

    # Find the thermistor (this should be moved to setup, no need to repeat every time)
    #device_file = device_folder[number] + '/w1_slave'

    # Read the temperature from the thermistor
    f = open(device_file[number], 'r')
    lines = f.readlines()
    f.close()

    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')

    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        # output temp_c
        temp = float(temp_string) / 1000.0

    return temp

def _MeanTemp(device_file, consistency_check=False):
    """
    
    """
    temp_list = list()
    for i in range(3):
        temp = _ReadThermistor(device_file, number=i)
        temp_list.append(temp)

    # Apply mean
    mean_temp = sum(temp_list) / 3

    if consistency_check:
        # Compute Difference of each value to the mean
        temp_diff = [x-mean_temp for x in temp_list]

        return temp_diff
    else:
        return mean_temp


def _Einmaischen(lcd, device_file, ein_temp):
    """

    """

    _LCD(lcd, str1='Erhitze zum', str2='Einmaischen')

    # Initially read temperature and time and create the first 10 values in one minute
    temp_record = list()
    time_record = list()
    for i in range(11):
        temp_record.append(_MeanTemp(device_file, consistency_check=False))
        time_record.append(datetime.datetime.now())

    time.sleep(2)
    while all(t < ein_temp for t in temp_record[-10:]):
        # Turn on socket cooker to heat
        A_status, B_status = _RemoteControlSocket(socket='A', on=True)

        # Get temperature and time
        temp_record.append(_MeanTemp(device_file, consistency_check=False))
        time_record.append(datetime.datetime.now())

        _LCD(lcd, str1='Soll: ' + str(ein_temp), str2='Ist: ' + str(round(temp_record[-1],2 )))
        time.sleep(5)
        _LCD(lcd, str1='Erhitze zum', str2='Einmaischen')


    # If temperature reached turn of cooker and wait for five minutes
    time.sleep(2)
    _LCD(lcd, str1='Temperatur', str2='Erreicht!')
    time.sleep(2)
    A_status, B_status = _RemoteControlSocket(socket='A', on=False)

    _LCD(lcd, str1='Jetzt', str2='Einmaischen!')

    # Wait 5mins
    now = datetime.datetime.now()
    end = now + datetime.timedelta(minutes=5)

    while now < end:
        time.sleep(.9)
        _LCD(lcd, str1='Einmaischen...', str2=str(end - now)[:7] + 'h')
        now = datetime.datetime.now()

        temp_record.append(_MeanTemp(device_file, consistency_check=False))
        time_record.append(datetime.datetime.now())

    _LCD(lcd, str1='Einmaischen', str2='Beendet...')
    time.sleep(5)

    return temp_record, time_record

def _Rasten(lcd, temp_record: list, time_record: list, rast_min: list, rast_temp: list, device_file: list,):
    """

    """
    _LCD(lcd, str1='Starte', str2='Rasten...')
    time.sleep(2)

    # Start Rasten
    for i in range(len(rast_min)):

        _LCD(lcd, str1='Heize zur naechsten' + str(i), str2='Rast')
        # Get current temperature
        for j in range(10):
            temp_record.append(_MeanTemp(device_file, consistency_check=False))
            time_record.append(datetime.datetime.now())

        # Heize zur n??chsten Rast, Puffer -0.25??C
        while any(t < (rast_temp[i] - 0.25) for t in temp_record[-10:]):
            # Turn cooker on
            A_status, B_status = _RemoteControlSocket(socket='A', on=True)

            # Read temperature and time
            temp_record.append(_MeanTemp(device_file, consistency_check=False))
            time_record.append(datetime.datetime.now())

            time.sleep(2)

            _LCD(lcd, str1='Soll: ' + str(rast_temp[i]), str2='Ist: ' + str(round(temp_record[-1], 2)))

        # Starte die Rast
        time.sleep(2)
        _CtrlLed(device='LED_rast', on=True)

        # Berechne Ende der Rast
        now = datetime.datetime.now()
        end = now + datetime.timedelta(minutes=rast_min[i])

        # Halte temperatur f??r die Zeit der Rast
        while time_record[-1] < end:
            # Get current time and temperature
            time_record.append(datetime.datetime.now())
            temp_record.append(_MeanTemp(device_file, consistency_check=False))

            _LCD(lcd, str1='Rast ' + str(i + 1) + '/ ' + str(len(rast_temp)), str2=str(end - time_record[-1])[:7] + 'h')
            time.sleep(3)
            _LCD(lcd, str1='Ist: ' + str(round(temp_record[-1], 2)) + 'C', str2='Soll: ' + str(rast_temp[i]) + 'C')

            # check if temperature has decreased below rast temperature
            if all(t < (rast_temp[i] - .25) for t in temp_record[-10:]):
                # turn on cooker for at least 30 seconds before next temperature measurement
                A_status, B_status = _RemoteControlSocket(socket='A', on=True)
                _CtrlLed(device='LED_socket_A', on=True)

                for j in range(10):
                    time_record.append(datetime.datetime.now())
                    temp_record.append(_MeanTemp(device_file, consistency_check=False))
                    time.sleep(3)

            else:
                A_status, B_status = _RemoteControlSocket(socket='A', on=False)







