import sqlite3
import logging
from typing import Tuple

from liteorm.tables import Table


class DataBase:

    def __init__(self, data_base_path=None) -> None:
        self.data_base_path = data_base_path or ':memory:'
        self.connect = sqlite3.connect(self.data_base_path)
        self.cursor = self.connect.cursor()

        self.logger = logging.getLogger('liteorm')
        self.logger.setLevel(logging.DEBUG)

    def create_table(self, table: Table, recreate=False) -> None:
        if recreate:
            self.drop_table(table)

        prepared_columns = table.columns_to_insert
        sql = ','.join(prepared_columns)
        try:
            self.cursor.execute(f'CREATE TABLE {table} ({sql})')
        except sqlite3.OperationalError:
            self.logger.warning(f'Table {table} already exists.')
        else:
            self.logger.info(f'Table {table} successfully created.')

    def drop_table(self, table: Table) -> None:
        self.cursor.execute(f'DROP TABLE {table}')
        self.logger.info(f'Table {table} successfuly deleted.')

    def insert(self, rows: Tuple[Table]) -> None:
        for row in rows:
            try:
                columns = []
                values = []
                for column in row.columns_names:
                    columns.append(column)
                    values.append(row.values[column])
                columns = ','.join(['?' for _ in columns])

                sql = f'INSERT INTO {row} VALUES ({columns})'
                self.cursor.execute(sql, values)
                self.logger.info(f'Record successfully inserted to {row}.')
            except sqlite3.IntegrityError as exc:
                self.logger.warning(f'Record already exists or "{exc}".')
                continue

        self.connect.commit()

    def update(self, schema, set_, where) -> None:
        sql_set = [f"{column}={value!r}" for column, value in set_.items()]
        sql_set = f"\n SET " + ', '.join(map(str, sql_set))

        sql_where = [f"{column}={value!r}" for column, value in where.items()]
        sql_where = f"\n WHERE " + ' and '.join(map(str, sql_where))

        sql = f'UPDATE {schema}' + sql_set + sql_where

        self.cursor.execute(sql)
        self.connect.commit()
        self.logger.info(f'Record {where} updated to {set_} from {schema} table.')

    def delete(self, table: Table, where_param) -> None:
        sql_query = [f'{column}={value!r}' for column, value in where_param.items()]
        sql_where = f'WHERE ' + ' and '.join(map(str, sql_query))
        sql = f'DELETE FROM {table} ' + sql_where
        self.cursor.execute(sql)
        self.connect.commit()
        self.logger.info(f'Record {where_param} deleted from {table} table.')

    def select(self, schema, join_schema=None, where_param=None) -> None:
        where_param = where_param or {1: 1}

        sql_where = [f"{column}={value!r}" for column, value in where_param.items()]
        sql_where = f"\n WHERE " + ' and '.join(map(str, sql_where))
        sql_join = ''

        if join_schema:
            fk = schema.get_foreign_key()
            sql_join = f'\n JOIN {join_schema} on {schema}.{fk[0]}={join_schema}.id'

        sql = f"SELECT * FROM {schema}\n" + sql_join + sql_where

        self.cursor.execute(sql)
        self.logger.debug(self.cursor.fetchall())
