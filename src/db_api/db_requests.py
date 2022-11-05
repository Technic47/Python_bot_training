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

    def create_table_basket(self, user_id):
        sql = """
        CREATE TABLE Basket(
        user_id int NOT NULL,
        basket text,
        PRIMARY KEY (user_id))"""
        self.execute(sql, commit=True)
        self.add_basket(user_id, "")

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

    def add_basket(self, user_id: int, basket: str = None):
        sql = """
        INSERT INTO Basket(user_id, basket) VALUES(?, ?)"""
        params = (user_id, basket)
        self.execute(sql, params, commit=True)

    def update_user_basket(self, user_id: int, item_id: str):
        old_item_id = self.select_user_basket(user_id=user_id)[0]
        new_item_id = f'{old_item_id} + " " + {item_id}'
        sql = "UPDATE Basket SET item_id=? WHERE id=?"
        return self.execute(sql, params=(new_item_id, user_id), commit=True)

    def add_item(self, id: int, quantity: int = 0, name: str = None, photo_path: str = ''):
        sql = """
        INSERT INTO Items(id, name, quantity, photo_path) VALUES(?, ?, ?, ?)"""
        params = (id, name, quantity, photo_path)
        self.execute(sql, params, commit=True)

    def select_user_info(self, **kwargs) -> list:
        sql = 'SELECT * FROM Users WHERE '
        sql, params = self.format_args(sql, kwargs)
        return self.execute(sql, params=params, fetchall=True)

    def select_user_basket(self, **kwargs) -> list:
        sql = 'SELECT * FROM Basket WHERE '
        sql, params = self.format_args(sql, kwargs)
        return self.execute(sql, params=params, fetchall=True)

    def select_item_info(self, **kwargs) -> list:
        sql = 'SELECT * FROM Items WHERE '
        sql, params = self.format_args(sql, kwargs)
        return self.execute(sql, params=params, fetchall=True)

    def select_all_users(self) -> tuple:
        sql = "SELECT * FROM Users"
        return self.execute(sql, fetchall=True)

    def select_all_items(self) -> tuple:
        sql = "SELECT * FROM Items"
        return self.execute(sql, fetchall=True)

    def delete_user(self, **kwargs):
        sql = "DELETE FROM Users WHERE "
        sql, params = self.format_args(sql, params=kwargs)
        return self.execute(sql, params=params, commit=True)

    def delete_item(self, **kwargs):
        sql = "DELETE FROM Items WHERE "
        sql, params = self.format_args(sql, params=kwargs)
        return self.execute(sql, params=params, commit=True)

    def delete_all_items(self):
        self.execute("DELETE FROM Items WHERE True", commit=True)

    def drop_all(self):
        self.execute("DROP TABLE Users", commit=True)

    def drop_all_items(self):
        self.execute("DROP TABLE Items", commit=True)

    def update_user_phone(self, id: int, phone: str):
        sql = "UPDATE Users SET phone=? WHERE id=?"
        return self.execute(sql, params=(phone, id), commit=True)

    def update_item_number(self, id: int, quantity: int):
        sql = "UPDATE Items SET quantity=? WHERE id=?"
        return self.execute(sql, params=(quantity, id), commit=True)

    def get_item_count(self) -> int:
        sql = "SELECT * FROM Items"
        return len(self.execute(sql, fetchall=True))

    @staticmethod
    def format_args(sql, params: dict) -> tuple:
        sql += " AND ".join([
            f"{item} = ?" for item in params
        ])
        return sql, tuple(params.values())
