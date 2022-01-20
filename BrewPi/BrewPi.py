# Main function for BrewPi

from .initialize_devices import Initialize
from .user_inputs import UserInputMaischenRasten
from .brewing_process import _Einmaischen

def BrewPi():
    """

    """

    lcd, device_file, ledPin_Socket_A, ledPin_Rest, ledPin_On, ledPin_End = Initialize()

    rast_min, rast_temp, ein_temp, ab_temp = UserInputMaischenRasten(lcd)

    temp_record, time_record = _Einmaischen(lcd, device_file, ein_temp)

    return


