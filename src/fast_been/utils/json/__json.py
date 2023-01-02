import json
from .json_encoders import Encoder


class JSON:

    @staticmethod
    def loads(value: str):
        return json.loads(value)

    @staticmethod
    def dumps(value: dict):
        return json.dumps(value, cls=Encoder)
