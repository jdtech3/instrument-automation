from pyvisa.errors import VisaIOError

from autometrology.errors import InstrumentNotFoundError
from autometrology.visa.pyvisa import VISA


class VISAUtils:
    @staticmethod
    def scan(visa: VISA, cmd: str, expected: str) -> str:
        # Scan
        for _id in visa.list():
            try:
                visa.open(_id)
                if expected in visa.query(cmd):
                    return _id
            except VisaIOError:
                pass

        raise InstrumentNotFoundError(
            "Scanning completed but no matching instrument found!"
        )

    @staticmethod
    def list_all(visa: VISA, cmds: list[str]) -> dict[str, str]:
        instruments = {}
        for _id in visa.list():
            for cmd in cmds:
                try:
                    visa.open(_id)
                    instruments[_id] = visa.query(cmd)
                    break
                except VisaIOError:
                    pass

        return instruments
