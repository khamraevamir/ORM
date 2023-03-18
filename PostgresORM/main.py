from orm import PostgresORM

database = PostgresORM (
    host='localhost',
    port=5432,
    user='postgres',
    password='123456',
    database='orm',
)

with database as db:
    # Create table
    # table_name = 'user'
    columns = {"name": "TEXT", "age": "INTEGER"}
    # db.create_table(table_name, columns)

    # Insert data
    # db.insert("users", data={"name": "John Doe", "age": 30})
    # db.insert("users", data={"name": "Jane Smith", "age": 25})
    # print(db.select("users"))

    # Select all columns
    # print(db.select("users"))

    # Select specific columns
    # print(db.select("users", columns=["name"]))

    # Select with WHERE clause
    # print(db.select("users", where={"age": 25}))

    # Select with ORDER BY clause
    # print(db.select("users", order_by="age DESC"))

    # Update data
    # db.update("users", set_values={"age": 35}, where={"name": "John Doe"})
    # print(db.select("users"))

    # Delete data
    # db.delete("users", {"name": "John Doe"})
    print(db.select("users"))


