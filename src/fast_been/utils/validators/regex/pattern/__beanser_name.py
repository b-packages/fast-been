from . import Base


class BeanserName(Base):
    @property
    def pattern(self):
        return "^(?!.*\.\.)(?!.*\.$)[^\W][\w.]{2,30}$"

    @property
    def info(self):
        return "Beansername can contain characters a-z," \
               " 0-9, underscores and periods. The username " \
               "cannot start with a period nor end with a " \
               "period. It must also not have more than one " \
               "period sequentially. Max length is 31chars."
