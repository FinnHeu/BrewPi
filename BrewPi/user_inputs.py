# Submodule for recieving user inputs
from .device_ctrl import _LCD

def _UserInputRasten():
    """Ask user in terminal to input length of Rasten

    Input
    -----

    Returns
    -------
    rast_min, list()
        Laenge der Rasten in Minute
    rast_temp: list()
        Temperaturen der Rasten in C

    """

    _LCD(lcd, str1='See Terminal for', str2='Instructions... ')

    # Input: Rasten Laenge
    user_input_1 = input('Laenge der Rasten in Minuten eingeben z.B. 10 30 20: ').split()

    rast_min = list()
    for _ in user_input_1:
        rast_min.append(float(_))

    # Input: Rasten Temperatur
    user_input_2 = input('Temperaturen der Rasten in Minuten eingeben, z.B. 60 65 87: ').split()

    rast_temp = list()
    for _ in user_input_2:
        rast_temp.append(float(_))

    if len(rast_min) != len(rast_temp):
        raise ValueError('Anzahl der Rasten und Temperaturen stimmen nicht ueberein!')

    return rast_min, rast_temp

def _UserInputEinAbmaischTemp():
    """
    Ask user in terminal to input Ein-/ Abmaisch temperature

    Input
    -----

    Returns
    -------
    ein_temp, list
        Einmaischtemperatur
    ab_temp, list
        Abmaischtemperatur
    """

    _LCD(lcd, str1='See Terminal for', str2='Instructions... ')

    # Input: Ein-/ Abmaischtemperatur
    user_input = input('Ein- und Abmaischtemperatur in C eingeben, z.B. 50 80: ').split()

    einab_temp = []  # type: List[float]
    for _ in user_input:
        einab_temp.append(float(_))

    if len(ein_temp) != 2:
        raise ValueError('Nur eine Einmaischtemperatur moeglich!')

    ein_temp = einab_temp[0]  # type: float
    ab_temp = einab_temp[-1]  # type: float

    return ein_temp, ab_temp

def UserInputMaischenRasten():
    """
    Main function for user inputs
    """
    rast_min, rast_temp = _UserInputRasten()
    ein_temp, ab_temp = _UserInputEinAbmaischTemp()

    return rast_min, rast_temp, ein_temp, ab_temp



