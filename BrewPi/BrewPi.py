# Main function for BrewPi

from .initialize_devices import Initialize
from .user_inputs import UserInputMaischenRasten
from .brewing_process import Brew

def BrewPi():
    """

    """

    lcd, device_file = Initialize()

    rast_min, rast_temp, ein_temp, ab_temp = UserInputMaischenRasten(lcd)

    temp_record, time_record = Brew(lcd, device_file, ein_temp, ab_temp, rast_min, rast_temp)

    return temp_record, time_record
