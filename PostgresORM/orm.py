import psycopg2


class PostgresORM:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    # Метод, который используется в контекстном менеджере (with)
    def __enter__(self):
        # При создании объекта, автоматически происходит подключение
        self.connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Автоматическое закрытие подключения с БД, не нужно использовать метод close()
        if self.connection:
            self.connection.close()
        if exc_type:
            raise exc_val

    def create_table(self, table_name, columns):
        try:
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("
            sql += "id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, "

            # Извлекаем из словаря название столбца и его значение
            for col_name, col_type in columns.items():
                sql += f"{col_name} {col_type}, "

            # Срез чтобы убрать запятую
            sql = sql[:-2] + ")"

            # Выполняем SQL-запрос
            self.cursor.execute(sql)
            self.connection.commit()

        except psycopg2.Error as e:
            print(f"Error while creating table: {str(e)}")

    def insert(self, table_name, data):
        try:
            # Извлекаем название столбцов из словаря
            keys = ", ".join(data.keys())
            placeholders = ", ".join("%s" for _ in data.values())
            # Извлекаем запись столбца из словаря
            values = tuple(data.values())
            sql = f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders})"
            self.cursor.execute(sql, values)
            self.connection.commit()
        except psycopg2.Error as e:
            print(f"Error while inserting data to table {table_name}: {e}")

    def select(self, table_name, columns=None, where=None, order_by=None):
        # Список колонок, которые будут запрошены в SQL-запросе
        if columns is None:
            columns = "*"
        columns = ", ".join(columns)

        sql = f"SELECT {columns} FROM {table_name}"

        # Условие WHERE
        if where is not None:
            # Извлечение столбцов из словаря, разделяя их по AND
            where_clause = " AND ".join([f"{k} = %s" for k in where.keys()])
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
            # Извлечение столбцов из каждой строки результата и создание словаря из этих значений
            # В результате метод вернет список словарей, где каждый словарь соответствует строке таблицы
            # Ключи словаря будут соответствовать названию столбцов, значения - соответствующим значениям из строки
            columns = [desc[0] for desc in self.cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except psycopg2.Error as e:
            print(f"Error while selecting from table {table_name}: {e}")

    def update(self, table_name, set_values, where):
        set_clause = ", ".join(f"{key} = %s" for key in set_values.keys())
        # Извлечение столбцов из словаря, разделяя их по AND
        where_clause = " AND ".join(f"{key} = %s" for key in where.keys())
        # Извлечение записи из словаря
        values = tuple(set_values.values()) + tuple(where.values())
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
        except psycopg2.Error as e:
            print(f"Error while updating from table {table_name}: {e}")
            self.connection.rollback()

    def delete(self, table_name, where):
        sql = f"DELETE FROM {table_name}"
        where_clause = ""
        values = []
        if where:
            # WHERE arg1 = ? AND arg2 = ?
            where_clause = " WHERE " + " AND ".join(f"{column} = %s" for column in where.keys())
            values = list(where.values())
        sql += where_clause
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
        except psycopg2.Error as e:
            print(f"Error while deleting from table {table_name}: {e}")