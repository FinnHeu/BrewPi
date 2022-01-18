#

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
    f = open(device_file, 'r')
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

    if not consistency_check:
        mean_temp = sum(temp_list) / 3
        return mean_temp
    else:
        return temp