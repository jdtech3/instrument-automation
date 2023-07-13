from time import sleep

from autometrology.lab.drivers import Keithley_2380_120_60

if __name__ == "__main__":
    inst = Keithley_2380_120_60()

    inst.disable()
    inst.power_load(5)
    inst.enable()

    while True:
        print(inst.get_voltage())
        sleep(0.2)

    # inst.disable()
    # inst.set_voltage(5)
    # inst.set_current(1)
    # inst.ocp(False)
    # inst.ovp(True)
    # sleep(2)
    # inst.enable()
    # while True:
    #     print(inst.get_voltage())
    #     print(inst.get_current())
    #     sleep(0.2)
