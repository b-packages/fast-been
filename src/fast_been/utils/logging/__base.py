from fast_been.api.cotrollers import Creator
from fast_been.api.models.logging import LogModel
from fast_been.conf.database import session_local
from fast_been.utils.macros import LogType


class Base(Creator):
    model = LogModel
    db = session_local()
    input_fields = [
        'type',
        'message',
    ]

    def info(self, message):
        input_data = {
            'type': LogType.info(),
            'message': message,
        }
        return self.run(input_data=input_data)

    def warning(self, message):
        input_data = {
            'type': LogType.warning(),
            'message': message,
        }
        return self.run(input_data=input_data)

    def error(self, message):
        input_data = {
            'type': LogType.error(),
            'message': message,
        }
        return self.run(input_data=input_data)


logger = Base()
