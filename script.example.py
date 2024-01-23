from time import sleep

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from datetime import datetime

from autometrology.lab.drivers import Keysight_34461A, Korad_KA3005P, Keithley_2380_120_60

if __name__ == "__main__":
    load = Keithley_2380_120_60()
    psu = Korad_KA3005P()
    dmm = Keysight_34461A()
    dmm.dc_voltage_mode()
    print(dmm.get_measurement())

    style.use('fivethirtyeight')

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs, ys = [], []
    plt.xlabel('Frame')
    plt.ylabel('Voltage (V)')
    plt.title('Live Graph')

    def animate(frame):
        # Add x and y to lists
        xs.append(frame)
        ys.append(dmm.get_measurement())
        ax.clear()
        ax.plot(xs, ys)
        ax.set_xlim(min(xs), max(xs))
        ax.set_ylim(min(ys) - 0.1, max(ys) + 0.1)

    ani = animation.FuncAnimation(fig, animate, interval=100, frames=100000)
    plt.show()

    # psu = Korad_KA3005P()

    # inst = Keithley_2380_120_60()
    #
    # inst.disable()
    # inst.power_load(5)
    # inst.enable()
    #

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
