class Service:
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

    __instance = None

    @property
    def instance(self):
        return self.__instance

    def get(self, **kwargs):
        self.__instance = self.queryset.filter(**kwargs).first()
        return self.__instance

    def list(self, page:int=1,page_size:int=1,filters:dict={},ordering:list=[]):
        list
        return self.queryset.filter(**filters).order_by(*ordering)
    def creator(self, data: dict):
        instance = self.model(**data)
        instance.__set_pid(data['pid'] if 'pid' in data else None)
        instance.__set_create_datetime()
        instance.__set_is_active()
        instance.__set_hashed()
        self.db.add(instance)
        self.db.commit()
        self.db.referesh(instance)
        self.__instance = instance
        return self.__instance

    def updator(self, pid: str, data: dict):
        # Get data from database
        self.get(pid=pid)
        if self.instance is None:
            return None
        self.__instance_deactivate()
        # Update data
        _data = data.copy()
        data = self.instance.to_dict().copy()
        data.update(_data)
        return self.creator(data)

    def destroyer(self, pid: str) -> None:
        # Get data from database
        self.get(pid=pid)
        if self.instance is None:
            return None
        # Disable data
        return self.__instance_deactivate()

    def __instance_deactivate(self):
        self.instance.is_active = False
        self.db.add(self.instance)
        self.db.commit()
        self.db.referesh(self.instance)
        self.__instance = None
        return self.instance
