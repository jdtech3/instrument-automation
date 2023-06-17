from pyvisa.errors import VisaIOError

from autometrology.lab.errors import InstrumentNotFoundError, InstrumentOpenError
from autometrology.lab.generic.dc_power_supply import DCPowerSupply


class Korad_KA3005P(DCPowerSupply):
    # -- Constructor
    def __init__(self, resource_id: str = None):
        super().__init__("Korad KA3005P", 0, 31.0, 0, 5.1)

        # Scan
        if resource_id is None:
            for _id in self.visa.list():
                try:
                    self.visa.open(_id)
                    if "KORAD KA3005P" in self.visa.query("*IDN?"):
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
        v = float(self.visa.query("VOUT1?"))
        return v

    def get_current(self) -> float:
        i = float(self.visa.query("IOUT1?"))
        return i

    def _set_voltage(self, v: float):
        self.visa.write(f"VSET1:{v}")

    def _set_current(self, i: float):
        self.visa.write(f"ISET1:{i}")

    def enable(self):
        self.visa.write("OUT1")

    def disable(self):
        self.visa.write("OUT0")

    def ovp(self, enable: bool):
        self.visa.write(f"OVP{1 if enable else 0}")

    def ocp(self, enable: bool):
        self.visa.write(f"OCP{1 if enable else 0}")

    def close(self):
        self.visa.close()
