import sqlite3


class SQLite3ORM:
    def __init__(self, db_path):
        # Путь к бд
        self.db_path = db_path
        self.connection = None

    # Метод который используется в контекстном менеджере(with)
    def __enter__(self):
        # При создании объекта, автоматом происходит подключение
        self.connection = sqlite3.connect(self.db_path)
        # Это нужно для того, чтобы мы могли вытаскивать записи в виде словаря
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Автоматическое закрытие подключения с бд, не нужно использовать метод close()
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        if exc_type:
            raise exc_val

    def create_table(self, table_name, columns):
        try:
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("
            sql += "id INTEGER PRIMARY KEY AUTOINCREMENT, "

            # Извлекаем из словаря название столбца и его значение
            for col_name, col_type in columns.items():
                sql += f"{col_name} {col_type}, "

            # Срез чтобы убрать запятую
            sql = sql[:-2] + ")"

            self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {str(e)}")

    def insert(self, table_name, data):
        try:
            # Извлекаем название столбцов из словаря
            keys = ", ".join(data.keys())
            placeholders = ", ".join("?" for _ in data.values())
            # Извлекаем запись столбца из словаря
            values = tuple(data.values())
            sql = f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders})"
            self.cursor.execute(sql, values)
            self.connection.commit()
        except Exception as e:
            print(f"Error while inserting data to table {table_name}: {e}")
            raise e

    def select(self, table_name, columns=None, where=None, order_by=None):
        # Список колонок, которые будут запрошены в SQL-запросе
        if columns is None:
            columns = "*"
        columns = ", ".join(columns)

        sql = f"SELECT {columns} FROM {table_name}"

        # Условие WHERE
        if where is not None:
            # Извлечение столбцов из словаря, разделяя их по AND
            where_clause = " AND ".join([f"{k} = ?" for k in where.keys()])
            # Извлечение записи из словаря
            where_values = tuple(where.values())
            sql += f" WHERE {where_clause}"
        else:
            where_values = ()

        # Сортировка
        if order_by is not None:
            sql += f" ORDER BY {order_by}"

        try:
            self.cursor.execute(sql, where_values)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error while selecting from table {table_name}: {e}")

    def update(self, table_name, set_values, where):
        set_clause = ", ".join(f"{key} = ?" for key in set_values.keys())
        # Извлечение столбцов из словаря, разделяя их по AND
        where_clause = " AND ".join(f"{key} = ?" for key in where.keys())
        # Извлечение записи из словаря
        values = tuple(set_values.values()) + tuple(where.values())
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error while updating from table {table_name}: {e}")
            self.connection.rollback()

    def delete(self, table_name, where):
        sql = f"DELETE FROM {table_name}"
        where_clause = ""
        values = []
        if where:
            # WHERE arg1 = ? AND arg2 = ?
            where_clause = " WHERE " + " AND ".join(f"{column} = ?" for column in where.keys())
            values = list(where.values())
        sql += where_clause
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error while deleting from table {table_name}: {e}")


