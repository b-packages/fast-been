from . import Base


class EmailAddress(Base):
    @property
    def pattern(self):
        return """
        [a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?
        """

    @property
    def info(self):
        return "Email Validation as per RFC2822 standards." \
               "- Straight from .net helpfiles :)"
