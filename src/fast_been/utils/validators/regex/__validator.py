import re


class Validator:
    pattern = None
    info = None

    def validate(self, value):
        return re.match(self.pattern, value)
