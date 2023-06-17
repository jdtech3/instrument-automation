from math import inf

from .instrument import Instrument


class ACVoltmeter(Instrument):
    # -- Properties
    min_voltage: float = -inf
    max_voltage: float = inf

    # -- Methods
    def measure_voltage(self):
        pass
