from math import inf

from .instrument import Instrument


class Voltmeter(Instrument):
    # -- Properties
    min_voltage_dc: float = -inf
    max_voltage_dc: float = inf
    min_voltage_ac: float = -inf
    max_voltage_ac: float = inf

    # -- Constructor
    def __init__(
        self,
        model: str,
        min_voltage_dc: float,
        max_voltage_dc: float,
        min_voltage_ac: float,
        max_voltage_ac: float,
    ):
        super().__init__(model)

        self.min_voltage_dc = min_voltage_dc
        self.max_voltage_dc = max_voltage_dc
        self.min_voltage_ac = min_voltage_ac
        self.max_voltage_ac = max_voltage_ac

    # -- Methods
    def measure_voltage_dc(self):
        pass

    def measure_voltage_ac(self):
        pass
