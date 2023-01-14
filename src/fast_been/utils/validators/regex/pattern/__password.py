from . import Base


class Password(Base):
    @property
    def pattern(self):
        return """
        ^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,31}$
        """

    @property
    def info(self):
        return " 8 characters - must contain at least 1 uppercase letter, 1 lowercase letter, and 1 number" \
               "- Can contain special characters"
