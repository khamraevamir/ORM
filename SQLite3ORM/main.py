from orm import SQLite3ORM

db_path = "example.db"

with SQLite3ORM(db_path) as db:
    # Create new table
    # db.create_table("users", columns={"name": "TEXT", "age": "INTEGER"})

    # Insert some data
    # db.insert("users", data={"name": "John Doe", "age": 30})
    # db.insert("users", data={"name": "Jane Smith", "age": 25})
    # print(db.select("users"))

    # Select all columns
    # print(db.select("users"))

    # Select specific columns
    # print(db.select("users", columns=["name"]))

    # Select with WHERE clause
    # print(db.select("users", where={"age": 30}))

    # Select with ORDER BY clause
    # print(db.select("users", order_by="age DESC"))

    # Update data
    # db.update("users", set_values={"age": 35}, where={"name": "John Doe"})
    # print(db.select("users"))

    # Delete data
    # db.delete("users", {"name": "John Doe"})
    print(db.select("users"))


