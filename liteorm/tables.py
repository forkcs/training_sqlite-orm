class Table:

    @classmethod
    def _get_name(cls):
        return cls.__name__.lower()

    @classmethod
    def _columns(cls):
        columns = []
        for k, v in cls.__dict__.items():
            if not k.startswith('__'):
                columns.append(f'{k} {" ".join(v)}')
        return ', '.join(columns)

    @classmethod
    def _column_names(cls):
        names = [k for k in cls.__dict__.keys() if not k.startswith('__')]
        return ', '.join(names)

    @classmethod
    def sql_string_create(cls) -> str:
        name = cls._get_name()
        columns = cls._columns()
        sql_string = f'CREATE TABLE {name} ({columns})'
        return sql_string

    @classmethod
    def sql_string_drop(cls) -> str:
        sql_string = f'DROP TABLE {cls._get_name()}'
        return sql_string

    @classmethod
    def sql_string_add_raw(cls, row: tuple) -> str:
        str_row = ', '.join(row)
        sql_string = f'INSERT INTO {cls._get_name()} ({cls._column_names()}) VALUES ({str_row})'
        return sql_string

