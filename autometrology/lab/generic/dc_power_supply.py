from math import inf

from .instrument import Instrument


class DCPowerSupply(Instrument):
    # -- Properties
    min_voltage: float = 0
    max_voltage: float = inf
    min_current: float = 0
    max_current: float = inf

    # -- Constructor
    def __init__(
        self,
        model: str,
        min_voltage: float,
        max_voltage: float,
        min_current: float,
        max_current: float,
    ):
        super().__init__(model)

        self.min_voltage = min_voltage
        self.max_voltage = max_voltage
        self.min_current = min_current
        self.max_current = max_current

    # -- Methods
    @Instrument.check_range(min_voltage, max_voltage)
    def set_voltage(self, v: float):
        try:
            return self._set_voltage(v)
        except AttributeError:
            raise NotImplementedError

    @Instrument.check_range(min_current, max_current)
    def set_current(self, i: float):
        try:
            return self._set_current(i)
        except AttributeError:
            raise NotImplementedError

    def enable(self):
        raise NotImplementedError

    def disable(self):
        raise NotImplementedError
