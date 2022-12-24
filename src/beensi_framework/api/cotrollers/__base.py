class __Base:
    def __init__(self, db, model):
        self.__db = db
        self.__model = model

    __db = None

    @property
    def db(self):
        return self.__db

    __model = None

    @property
    def model(self):
        return self.__model

    __queryset = None

    @property
    def queryset(self):
        if self.__queryset is None:
            self.__queryset = self.db.query(self.model).filter(is_active=True).all()
        return self.__queryset
