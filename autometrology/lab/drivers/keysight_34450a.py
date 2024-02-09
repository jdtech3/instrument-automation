import logging

from pyvisa.errors import VisaIOError

from autometrology.errors import InstrumentOpenError
from autometrology.lab.generic.voltmeter import Voltmeter
from autometrology.visa.utils import VISAUtils

# ! TODO: INCOMPLETE!!


class Keysight_34450A(Voltmeter):
    # -- Constructor
    def __init__(self, resource_id: str = None):
        super().__init__("Keysight 34450A", 0, 1000, 0, 750)

        # Scan
        if resource_id is None:
            resource_id = VISAUtils.scan(self.visa, "*IDN?", "34450A")

        # Open
        try:
            self.visa.open(resource_id)
        except VisaIOError as e:
            raise InstrumentOpenError(str(e))

        # Config
        self.visa.resource.read_termination = "\n"
        self.visa.resource.write_termination = "\n"

        logging.info(self.visa.query("*IDN?").replace("\n", " ") + "loaded!")

    # -- Methods

    def dc_voltage_mode(self) -> float:
        return self.visa.write("CONF:VOLT:DC")

    def get_measurement(self) -> float:
        resp = self.visa.query("READ?")
        return float(resp)

    def self_test(self) -> bool:
        resp = self.visa.query("TEST:ALL?")
        return resp == '+0'

    def close(self):
        self.visa.write("SYST:LOC")
        self.visa.close()
