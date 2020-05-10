import sqlite3
import logging

from liteorm.log import get_orm_logger


class Database:

    def __init__(self, db_path: str = ':memory:') -> None:
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        self.logger = get_orm_logger(log_level=logging.DEBUG)

    def save(self) -> None:
        self.conn.commit()

    def exit(self):
        self.cursor.close()
        self.conn.close()

    ##########
    # TABLES #
    ##########

    def create_table(self, table, soft=True) -> None:
        """Create table by Table object"""

        try:
            query = table.sql_string_create()
            self.logger.debug(f'Executing query: {query}')
            self.cursor.execute(query)
        except sqlite3.OperationalError:
            if soft:
                return
            else:
                self.drop_table(table)
                self.create_table(table)

    def drop_table(self, table) -> None:
        query = table.sql_string_drop()
        self.logger.debug(f'Executing query: {query}')
        self.cursor.execute(query)

    ########
    # Data #
    ########

    def add_row(self, table, row: tuple):
        query = table.sql_string_add_raw(row=row)
        self.logger.debug(f'Executing query: {query}')
        self.cursor.execute(query)

    def delete_rows(self, table, where: str = None):
        query = table.sql_string_delete_rows(where=where)
        self.logger.debug(f'Executing query: {query}')
        self.cursor.execute(query)
