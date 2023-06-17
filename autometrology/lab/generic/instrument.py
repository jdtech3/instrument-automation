from functools import wraps

from autometrology.visa.pyvisa import VISA
from ..errors import OutOfRangeError

class Instrument():
    # -- Properties
    model: str = 'Generic Instrument'
    visa: VISA = None

    # -- Constructor
    def __init__(self, model: str):
        self.model = model
        self.visa = VISA()

    # -- Decorators
    @staticmethod
    def check_range(min: float, max: float):
        def _check_range(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                if (min <= args[1] <= max):
                    return f(*args, **kwargs)
                else:
                    raise OutOfRangeError(f'Expecting between {min} and {max}, but got {args[1]}')
                
            return wrapper

        return _check_range     # as per https://stackoverflow.com/questions/5929107/decorators-with-parameters
