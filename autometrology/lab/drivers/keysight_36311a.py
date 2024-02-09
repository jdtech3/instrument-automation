import logging

from pyvisa.errors import VisaIOError

from autometrology.errors import ChannelError, InstrumentOpenError
from autometrology.lab.generic.dc_power_supply import DCPowerSupply
from autometrology.visa.utils import VISAUtils

# ! TODO: INCOMPLETE!!


class Keysight_36311A(DCPowerSupply):
    # -- Constructor
    def __init__(self, resource_id: str = None):
        super().__init__("Keysight 36311A", 0, 30.9, 0.001, 1.03)

        # Scan
        if resource_id is None:
            resource_id = VISAUtils.scan(self.visa, "*IDN?", "36311A")

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
    def _set_voltage(self, v: float):
        self.visa.write(f"VOLT {v}")

    def _set_current(self, i: float):
        self.visa.write(f"CURR {i}")

    def select_channel(self, channel: int):
        if channel not in [1, 2, 3]:
            raise ChannelError(f"Expecting channel 1, 2, or 3 but got {channel}")

        self.visa.write(f"INST:NSEL {channel}")

    def enable(self):
        self.visa.write("OUTP ON")

    def disable(self):
        self.visa.write("OUTP OFF")

    def close(self):
        self.visa.write("SYST:LOC")
        self.visa.close()
