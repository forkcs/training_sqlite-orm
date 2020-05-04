from liteorm.db import Database
from liteorm.tables import Table


class User(Table):
    user_id = ('INTEGER', 'NOT_NULL')
    name = ('CHAR', 'NOT_NULL')


if __name__ == '__main__':
    db = Database(db_path='db.sqlite3')
    db.create_table(User, soft=False)  # recreate if table already exists

    db.add_row(User, ('228', "'GEOSAS Admin'"))
    db.add_row(User, ('229', "'GEOSAS User'"))

