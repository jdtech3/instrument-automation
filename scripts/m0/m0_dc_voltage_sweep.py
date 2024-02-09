from dataclasses import dataclass
import pandas as pd
import numpy as np
import logging
import time

from autometrology.lab.drivers import (
    Keysight_36311A,        # PSU
    Keysight_34450A,        # Multimeter
)


"""
ECE295 M0 DC voltage sweep (line regulation) test:

Sweeps voltage from set minimum and maximums, recording: V_in, V_out

Built to use:
  - DMM: Keysight 34450A
  - PSU: Keysight 36311A
"""


# SET THIS!
DMM_IP = '192.168.2.2'
PSU_IP = '192.168.2.3'


@dataclass
class TestParameters:
    min_vin: float
    max_vin: float
    vin_increment: float
    # expected_vout: float
    settling_time: float


class Result:
    vin: float
    vout: float

    def __init__(self, vin: float, vout: float):
        self.vin = vin
        self.vout = vout


class Results(object):
    raw: list[Result] = []

    def get_df(self) -> pd.DataFrame:
        df = pd.DataFrame(columns=["Vin", "Vout"])

        i = 0
        for result in self.raw:
            df.loc[i] = [result.vin, result.vout]
            i += 1

        return df


def take_input() -> TestParameters:
    print("Enter values or press enter to accept defaults:\n")

    min_vin = float(input("Minimum VIN volts [0]: ") or "0")
    max_vin = float(input("Maximum VIN volts [30]: ") or "30")
    vin_increment = float(input("Increment VIN by volts [0.5]: ") or "0.5")
    settling_time = float(input("Settling time between setting and measurement seconds [0.5]: ") or "0.5")

    return TestParameters(
        min_vin=min_vin,
        max_vin=max_vin,
        vin_increment=vin_increment,
        settling_time=settling_time,
    )


def verify_input(params: TestParameters) -> bool:
    print("\nYou entered the following values:\n")
    print("Min VIN:", params.min_vin, "Max VIN:", params.max_vin, "VIN increment:", params.vin_increment)
    print("Settling time:", params.settling_time)

    accept = input("\nAccept (y/n)? ") == 'y'
    print("\n")
    return accept


def sweep(params: TestParameters, psu: Keysight_36311A, dmm: Keysight_34450A) -> Results:
    logging.warning(f"Starting sweep from {params.min_vin} V to {params.max_vin} V!")

    psu.set_voltage(psu.min_voltage)
    psu.set_current(psu.max_current)
    psu.enable()

    dmm.dc_voltage_mode()

    results = Results()
    for vin in np.arange(params.min_vin, params.max_vin + params.vin_increment, params.vin_increment):
        psu.set_voltage(vin)
        time.sleep(params.settling_time)

        measured_vout = dmm.get_measurement()

        results.raw.append(Result(
            vin=vin,
            vout=measured_vout,
        ))

        logging.info(f"IN: {vin} V; OUT: {measured_vout} V")

    psu.disable()

    return results


def run():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s.%(msecs)03d :: %(levelname)-8s :: %(message)s", datefmt="%H:%M:%S")

    logging.info("Initializing instruments")
    psu = Keysight_36311A(resource_id=f"TCPIP::{PSU_IP}::inst0::INSTR")
    dmm = Keysight_34450A(resource_id=f"TCPIP::{DMM_IP}::inst0::INSTR")

    params = take_input()
    while not verify_input(params):
        params = take_input()

    results = sweep(params, psu, dmm)
    df = results.get_df()
    df.to_csv("out.csv")


if __name__ == '__main__':
    run()
