# Main function for BrewPi

from .initialize_devices import Initialize
from .user_inputs import UserInputMaischenRasten

def BrewPi():
    """

    """

    lcd, device_file = Initialize()

    rast_min, rast_temp, ein_temp, ab_temp = UserInputMaischenRasten(lcd)


    return


