# Main function for BrewPi

from BrewPi.initialize_devices import Initialize
from BrewPi.user_inputs import UserInputMaischenRasten

def BrewPi():
    """

    """

    lcd, device_file = Initialize()

    rast_min, rast_temp, ein_temp, ab_temp = UserInputMaischenRasten()

    return


if __name__ == '__main__':

    try:
        BrewPi()
    except KeyboardInterrupt:
        GPIO.cleanup()





