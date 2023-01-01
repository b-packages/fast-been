from fastapi import Response, Request


class Base:
    request: Request = None
    response: Response = None
    controller_class = None
    is_login: bool = False

    def run(self, **kwargs):
        if self.__is_login_check:
            return self.__controller.run(**kwargs)

    @property
    def __controller(self):
        return self.controller_class()

    @property
    def __is_login_check(self):
        if self.is_login:
            # ...
            pass
        return True
