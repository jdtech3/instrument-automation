from typing import List, Union

import pyvisa


class VISA:
    def __init__(self):
        self.rm: pyvisa.ResourceManager = pyvisa.ResourceManager()
        self.resource: Union[pyvisa.Resource, None] = None

    def list(self) -> List:
        return list(self.rm.list_resources())

    def open(self, name: str):
        self.resource = self.rm.open_resource(name)
        return self.resource

    def close(self):
        return self.resource.close()

    def query(self, cmd: str):
        return self.resource.query(cmd)

    def write(self, cmd: str):
        return self.resource.write(cmd)
