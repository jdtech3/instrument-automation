from .instrument import Instrument
from math import inf

class DCVoltmeter(Instrument):
    # -- Properties
    min_voltage: float = -inf
    max_voltage: float = inf

    # -- Methods
    def measure_voltage(self):
        pass
