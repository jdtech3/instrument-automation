from pyvisa.errors import VisaIOError

from autometrology.lab.errors import InstrumentNotFoundError, InstrumentOpenError
from autometrology.lab.generic.dc_load import DCLoad


class Keithley_2380_120_60(DCLoad):
    # -- Constructor
    def __init__(self, resource_id: str = None):
        super().__init__("Keithley 2380-120-60", 0, 120.0, 0, 60.0, 0, 7500)

        # Scan
        if resource_id is None:
            for _id in self.visa.list():
                try:
                    self.visa.open(_id)
                    if "2380-120-60" in self.visa.query("*IDN?"):
                        resource_id = _id
                except VisaIOError:
                    pass

            if resource_id is None:
                raise InstrumentNotFoundError(
                    "Scanning completed but no matching instrument found!"
                )

        # Open
        try:
            self.visa.open(resource_id)
        except VisaIOError as e:
            raise InstrumentOpenError(str(e))

        print(self.visa.query("*IDN?").replace("\n", ""), "loaded!")

    # -- Methods
    def get_voltage(self) -> float:
        v = float(self.visa.query("MEAS:VOLT?"))
        return v

    def get_current(self) -> float:
        i = float(self.visa.query("MEAS:CURR?"))
        return i

    def get_power(self) -> float:
        i = float(self.visa.query("MEAS:POW?"))
        return i

    def current_load(self, i: float):
        self.visa.write("FUNC CURR")
        self.visa.write(f"CURR {i}")

    def resistance_load(self, r: float):
        self.visa.write("FUNC RES")
        self.visa.write(f"RES {r}")

    def voltage_load(self, v: float):
        self.visa.write("FUNC VOLT")
        self.visa.write(f"VOLT {v}")

    def power_load(self, p: float):
        self.visa.write("FUNC POW")
        self.visa.write(f"POW {p}")

    def short_load(self, enable: bool):
        self.visa.write(f"INP:SHOR {1 if enable else 0}")

    def enable(self):
        self.visa.write("SOUR:INP ON")

    def disable(self):
        self.visa.write("SOUR:INP OFF")

    def close(self):
        self.visa.write("SYST:LOC")
        self.visa.close()
