# Main function for BrewPi

from ctrl_hardware.initialize_devices import Initialize
from ctrl_user.user_inputs import UserInputMaischenRasten
from ctrl_brewing.brewing_process import Brew


def run():
    """

    """

    lcd, device_file = Initialize()

    rast_min, rast_temp, ein_temp, ab_temp = UserInputMaischenRasten(lcd)

    temp_record, time_record = Brew(lcd, device_file, ein_temp, ab_temp, rast_min, rast_temp)

    return temp_record, time_record

if __name__ == '__main__':
    run()
