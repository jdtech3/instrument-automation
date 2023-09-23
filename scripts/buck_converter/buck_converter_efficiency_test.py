from dataclasses import dataclass
import pandas as pd
import numpy as np
import logging
import time

from autometrology.lab.drivers import (
    Korad_KA3005P,          # PSU
    Keithley_2380_120_60,   # E-Load
    Keysight_34461A,        # Multimeter
)


"""
Buck converter efficiency test:

Sweeps voltage and current from set minimum and maximums, recording: V_in, V_out, I_in, I_out
More details here: https://utat-ss.notion.site/Joe-s-Buck-Efficiency-Test-Plan-e294c701bbd345b1b5c957562f6f9c31

Built to use:
  - DMM: Keysight 34461A
  - PSU: KORAD KA3005P
  - LOAD: Keithley 2380-120-60
"""


@dataclass
class TestParameters:
    min_vin: float
    max_vin: float
    vin_increment: float
    min_iout: float
    max_iout: float
    iout_increment: float
    settling_time: float


class Result:
    vin: float
    iin: float
    vout: float
    iout: float

    def __init__(self, vin: float, iin: float, vout: float, iout: float):
        self.vin = vin
        self.iin = iin
        self.vout = vout
        self.iout = iout

    def get_efficiency(self) -> float:
        return (self.vout * self.iout) / (self.vin * self.iin)


class Results(object):
    raw: list[Result] = []

    def get_efficiency_df(self) -> pd.DataFrame:
        df = pd.DataFrame(columns=["Vin", "Iout", "Efficiency"])

        i = 0
        for result in self.raw:
            df.loc[i] = [result.vin, result.iout, result.get_efficiency()]
            i += 1

        return df


def take_input() -> TestParameters:
    print("Enter values or press enter to accept defaults:\n")

    min_vin = float(input("Minimum VIN volts [7]: ") or "7")
    max_vin = float(input("Maximum VIN volts [17]: ") or "17")
    vin_increment = float(input("Increment VIN by volts [1]: ") or "1")
    min_iout = float(input("Minimum IOUT amps [0]: ") or "0")
    max_iout = float(input("Maximum IOUT amps [5]: ") or "5")
    iout_increment = float(input("Increment IOUT by amps [0.5]: ") or "0.5")
    settling_time = float(input("Settling time between setting and measurement seconds [0.5]: ") or "0.5")

    return TestParameters(
        min_vin=min_vin,
        max_vin=max_vin,
        vin_increment=vin_increment,
        min_iout=min_iout,
        max_iout=max_iout,
        iout_increment=iout_increment,
        settling_time=settling_time,
    )


def verify_input(params: TestParameters) -> bool:
    print("\nYou entered the following values:\n")
    print("Min VIN:", params.min_vin, "Max VIN:", params.max_vin, "VIN increment:", params.vin_increment)
    print("Min IOUT:", params.min_iout, "Max IOUT:", params.max_iout, "IOUT increment:", params.iout_increment)
    print("Settling time:", params.settling_time)

    accept = input("\nAccept (y/n)? ") == 'y'
    print("\n")
    return accept


def sweep(params: TestParameters, psu: Korad_KA3005P, load: Keithley_2380_120_60, dmm: Keysight_34461A) -> Results:
    logging.warning(f"Starting sweep from {params.min_vin} V to {params.max_vin} V and {params.min_iout} A to {params.max_iout} A!")

    psu.set_voltage(0)
    psu.set_current(psu.max_current)
    psu.enable()

    load.current_load(0)
    load.remote_sense(True)
    load.enable()

    dmm.dc_voltage_mode()

    results = Results()
    for vin in np.arange(params.min_vin, params.max_vin + params.vin_increment, params.vin_increment):
        logging.info(f"-- VIN: {vin} V --")

        psu.set_voltage(vin)
        time.sleep(params.settling_time)

        for iout in np.arange(params.min_iout, params.max_iout + params.iout_increment, params.iout_increment):
            if iout == 0:
                iout = 0.1

            load.current_load(iout)
            time.sleep(params.settling_time)

            measured_vin = dmm.get_measurement()
            measured_iin = psu.get_current()
            measured_vout = load.get_voltage()
            measured_iout = load.get_current()

            results.raw.append(Result(
                vin=measured_vin,
                iin=measured_iin,
                vout=measured_vout,
                iout=measured_iout,
            ))

            logging.info(f"IN: {measured_vin} V, {measured_iin} A; OUT: {measured_vout} V, {measured_iout} A")

    psu.disable()
    load.disable()

    return results


def run():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s.%(msecs)03d :: %(levelname)-8s :: %(message)s", datefmt="%H:%M:%S")

    logging.info("Initializing instruments")
    psu = Korad_KA3005P()
    load = Keithley_2380_120_60()
    dmm = Keysight_34461A()

    params = take_input()
    while not verify_input(params):
        params = take_input()

    results = sweep(params, psu, load, dmm)
    df = results.get_efficiency_df()
    df.to_csv("out.csv")


if __name__ == '__main__':
    run()
