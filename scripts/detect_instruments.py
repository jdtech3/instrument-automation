from autometrology.visa.pyvisa import VISA
from autometrology.visa.utils import VISAUtils


if __name__ == '__main__':
    visa = VISA()
    instruments = VISAUtils.list_all(visa, ['*IDN?'])

    for _id, response in instruments.items():
        print('Found', response, 'at', _id)
