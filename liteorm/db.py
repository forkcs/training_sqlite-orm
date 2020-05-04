import sqlite3
import logging


class Database:

    def __init__(self, db_path: str = ':memory:') -> None:
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        logging.basicConfig()
        self.logger = logging.getLogger('liteorm')
        self.logger.setLevel(logging.DEBUG)

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
