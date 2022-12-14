import sqlite3


class DB:
    def __init__(self, path_db: str):
        self.path_db = path_db

    @property  # превращает метод в аналог поля
    def connection(self):
        return sqlite3.connect(self.path_db)

    def execute(self, sql: str, params: tuple = tuple(),
                fetchone=False, fetchall=False, commit=False):
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, params)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users(
        id int NOT NULL,
        phone text,
        PRIMARY KEY (id))"""
        self.execute(sql, commit=True)

    def create_table_basket(self):
        sql = """
        CREATE TABLE Basket(
        user_id int NOT NULL,
        start text,
        PRIMARY KEY (user_id))"""
        self.execute(sql, commit=True)

    def create_table_items(self):
        sql = """
        CREATE TABLE Items(
        id int NOT NULL,
        name text,
        quantity int,
        photo_path text,
        PRIMARY KEY (id))"""
        self.execute(sql, commit=True)

    def add_user(self, id: int, phone: str = None):
        sql = """
        INSERT INTO Users(id, phone) VALUES(?, ?)"""
        params = (id, phone)
        self.execute(sql, params, commit=True)

    def add_basket(self, user_id: int, basket: str = ''):
        self.add_user(id=user_id, phone='')
        sql = """
        INSERT INTO Basket(user_id, start) VALUES(?, ?)"""
        params = (user_id, basket)
        self.execute(sql, params, commit=True)

    def select_user_basket(self, **kwargs) -> list:
        sql = f'SELECT * FROM Basket WHERE '
        sql, params = self.format_args(sql, kwargs)
        data = self.execute(sql, params=params, fetchone=True)
        if data is None:
            self.add_user(id=kwargs['user_id'], phone='')
            self.add_basket(user_id=kwargs['user_id'])
            data = (kwargs['user_id'], '')
        return data

    def update_user_basket(self, user_id: int, basket: str):
        sql = "UPDATE Basket SET basket=? WHERE user_id=?"
        return self.execute(sql, params=(basket, user_id), commit=True)

    def clear_basket(self, user_id: int) -> None:
        clear_basket = f''
        sql = "UPDATE Basket SET basket=? WHERE user_id=?"
        return self.execute(sql, params=(clear_basket, user_id), commit=True)

    def add_item(self, id: int, quantity: int = 0, name: str = None, photo_path: str = ''):
        sql = """
        INSERT INTO Items(id, name, quantity, photo_path) VALUES(?, ?, ?, ?)"""
        params = (id, name, quantity, photo_path)
        self.execute(sql, params, commit=True)

    def select_info(self, table: str, **kwargs) -> list:
        sql = f'SELECT * FROM {table} WHERE '
        sql, params = self.format_args(sql, kwargs)
        return self.execute(sql, params=params, fetchall=True)

    def select_all(self, table: str):
        sql = f"SELECT * FROM {table}"
        return self.execute(sql, fetchall=True)

    def delete(self, table: str, **kwargs):
        sql = f"DELETE FROM {table} WHERE "
        sql, params = self.format_args(sql, params=kwargs)
        return self.execute(sql, params=params, commit=True)

    def delete_all(self, table: str):
        self.execute(f"DELETE FROM {table} WHERE True", commit=True)

    def drop_all(self, table: str):
        self.execute(f"DROP TABLE {table}", commit=True)

    def update_user_phone(self, id: int, phone: str):
        sql = "UPDATE Users SET phone=? WHERE id=?"
        return self.execute(sql, params=(phone, id), commit=True)

    def update_item_number(self, id: int, quantity: int):
        sql = "UPDATE Items SET quantity=? WHERE id=?"
        return self.execute(sql, params=(quantity, id), commit=True)

    @staticmethod
    def format_args(sql, params: dict) -> tuple:
        sql += " AND ".join([
            f"{item} = ?" for item in params
        ])
        return sql, tuple(params.values())
