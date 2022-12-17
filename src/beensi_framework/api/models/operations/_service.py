class Service:
    model = None
    db = None
    _query = None

    def __init__(self, db, model):
        self.db = db
        self.model = model

    def query(self):
        if self._query:
            return self._query
        self._query = self.db.query(self.model).filter(is_active=True).all()
        return self._query

    _data = None

    def data(self, input_data: dict) -> dict:
        self._data = input_data

    def there_is(self, **kwargs) -> bool:
        tmp = self.query().filter(**kwargs).all()
        return bool(len(tmp))

    def get(self, **kwargs):
        return self.query().filter(**kwargs).first()

    def __valid_data(self) -> dict | None:
        if self._data is None:
            return None
        if not len(self._data):
            return None
        return self._data

    def creator(self):
        if not self.__valid_data():
            return None
        obj = self.model(**self._data)
        obj.__set_pid()
        obj.__set_create_datetime()
        obj.__set_is_active()
        obj.__set_hashed()
        self.db.add(obj)
        self.db.commit()
        self.db.referesh(obj)
        return obj

    def updator(self, pid: str):
        if not self.__valid_data():
            return None
        # Get data from database
        obj = self.get(pid=pid)
        if obj is None:
            return None
        data = obj.to_dict()
        # Disable data
        obj.is_active = False
        self.db.add(obj)
        self.db.commit()
        self.db.referesh(obj)

        # Update data
        data.update(self._data)
        new_obj = self.model(**data)
        new_obj.pid = data['pid']
        new_obj.__set_create_datetime()
        new_obj.__set_is_active()
        new_obj.__set_hashed()
        self.db.add(new_obj)
        self.db.commit()
        self.db.referesh(new_obj)
        return new_obj

    def destroyer(self, pid: str) -> None:
        # Get data from database
        obj = self.get(pid=pid)
        if obj is None:
            return None
        # Disable data
        obj.is_active = False
        self.db.add(obj)
        self.db.commit()
        self.db.referesh(obj)
        return None
