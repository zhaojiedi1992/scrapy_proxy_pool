import json

import attrs


@attrs.define
class Proxy(object):
    """
    proxy schema
    """
    host: str
    port: int=80
    username: str=None
    password: str=None

    def __str__(self):
        """
        to string, for print
        :return:
        """
        if self.username and self.password:
            return f'{self.username}:{self.password}@{self.host}:{self.port}'
        return f'{self.host}:{self.port}'

    def string(self):
        """
        to string
        :return: <host>:<port>
        """
        return self.__str__()

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {"host":self.host,"port":self.port,"proxy": f'{self.host}:{self.port}'}

