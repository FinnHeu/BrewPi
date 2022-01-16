# Main function for BrewPi

from initialize_devices import Initialize
from user_inputs import UserInputMaischenRasten

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





