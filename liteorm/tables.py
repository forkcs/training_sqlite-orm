class Table:
    __table_name__ = ''

    id = ('INTEGER', 'PRIMARY KEY', 'AUTOINCREMENT')

    def __init__(self, **kwargs) -> None:
        self._values = kwargs
        if 'id' not in kwargs:
            self._values['id'] = None

    @staticmethod
    def _is_field(key: str) -> bool:
        if key.startswith('__'):
            return False
        if key.endswith('__'):
            return False
        return True

    @property
    def columns_to_insert(self):
        field_names = [f'{k} {" ".join(v)}' for k, v in self.__class__.__dict__.items()
                       if self._is_field(k)]
        return field_names

    @property
    def columns_names(self):
        field_names = [f'{k if k != "key" else ""}' for k in self.__class__.__dict__.keys()
                       if self._is_field(k)]
        return field_names

    @property
    def values(self):
        return self._values

    def get_foreign_key(self):
        field_names = [f'{column}' for column, value in self.__class__.__dict__.items()
                       if self._is_field(column) and 'REFERENCES' in value]
        return field_names

    def __str__(self):
        return self.__table_name__
