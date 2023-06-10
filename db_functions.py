import sqlite3, contextlib
from lib_functions import get_salt, encode
from lib_globals import dbname


def connect_db():
    return sqlite3.connect(dbname)


def execute(query, values=None, cursor_callback=None):
    try:
        with contextlib.closing(sqlite3.connect(dbname)) as conn:  # auto-closes
            with conn:  # auto-commits
                with contextlib.closing(conn.cursor()) as cursor:  # auto-closes
                    if values is None:
                        cursor.execute(query)
                    else:
                        cursor.execute(query, values)
                    if cursor_callback is not None:
                        # print(f"cb: {cursor_callback(cursor)}")
                        return cursor_callback(cursor)

    except Exception as e:
        print(f"Execute error: {e}, query: {query}, values: {values}")


def commit(query, values=None):
    try:
        with contextlib.closing(sqlite3.connect(dbname)) as conn:  # auto-closes
            with conn:  # auto-commits
                with contextlib.closing(conn.cursor()) as cursor:  # auto-closes
                    if values is None:
                        cursor.execute(query)
                    else:
                        cursor.execute(query, values)
                    cursor.commit()
    except Exception as e:
        print(f"Commit error: {e}")


# fetching
def cb_fetchall(cursor):
    all_res = cursor.fetchall()
    return all_res


def cb_fetchone(cursor):
    one_res = cursor.fetchone()
    # print(f"fone: {fetchone_res}")
    return one_res  # cursor.fetchone()


def fetchall(table, columns="*", condition=None, order=None, order_col=None):
    cond = "" if condition == None else f" WHERE {condition}"
    sort = (
        "" if order == None or order_col == None else f" ORDER BY {order_col} {order}"
    )
    query = f"SELECT {columns} FROM {table}{cond}{sort}"

    return execute(query=query, cursor_callback=cb_fetchall)


def fetchone(table, columns="*", condition=None, order=None, order_col=None):
    cond = "" if condition == None else f" WHERE {condition}"
    sort = (
        "" if order == None or order_col == None else f" ORDER BY {order_col} {order}"
    )
    query = f"SELECT {columns} FROM {table}{cond}{sort}"

    return execute(query=query, cursor_callback=cb_fetchone)


def table_exists(table_name):
    # Check if the table exists
    return execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'",
        cb_fetchone,
    )


def row_count(table_name):
    # Count the number of rows
    with execute(f"SELECT COUNT(*) FROM {table_name}") as cursor:
        return cursor.fetchone()[0]


def aggregate(self, table_name, aggregate="COUNT"):
    with execute(f"SELECT {aggregate}(*) FROM {table_name}") as cursor:
        return cursor.fetchone()[0]


def join2tables(table1, table2, column, join_type):
    with execute(
        f"SELECT * FROM {table1} {join_type} {table2} ON {table1}.{column} = {table2}.{column}"
    ) as cursor:
        return cursor.fetchall()


def insert(table, data):
    # usage:
    # data = {
    #     'name': 'John Doe',
    #     'age': 25,
    #     'city': 'New York'
    # }

    # insert('students', data)

    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    print(f"columns: {columns}")
    print(f"placeholders: {placeholders}")

    insert_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

    values = tuple(data.values())

    commit(insert_query, values)


def update(table, data, id):
    # usage:
    # data = {
    #     'name': 'Jane Smith',
    #     'age': 30,
    #     'city': 'Los Angeles'
    # }
    # id = 1

    # update('students', data, id)

    set_values = ", ".join([f"{column} = ?" for column in data.keys()])

    update_query = f"UPDATE {table} SET {set_values} WHERE id = ?"

    values = tuple(list(data.values()) + [id])

    commit(update_query, values)


def upsert(table, data, condition=None):
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    values = tuple(data.values())
    operation = "UPDATE"

    def insert():
        insert_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        commit(insert_query, values)

    if condition:
        update_query = (
            f"UPDATE {table} SET {columns} = {placeholders} WHERE {condition}"
        )
        with commit(update_query, values) as cursor:
            if cursor.rowcount <= 0:
                insert()
                operation = "INSERT"
    else:
        insert()
        operation = "INSERT"

    print(f"{operation} committed")


def delete(table, condition):
    commit(f"DELETE FROM {table} WHERE {condition}")


def drop(table):
    # Drop a table
    commit(f"DROP TABLE IF EXISTS {table}")


# def abort(db_operation=None):
#     # Abort/rollback the changes and close the connection
#     try:
#         if db_operation is not None:
#             # Perform your database operations
#             # ...
#             db_operation()
#             # Rollback the transaction
#             self.connection.rollback()

#     except Exception as e:
#         # Handle any exceptions that occurred during the transaction
#         print("Error:", str(e))
#         self.connection.rollback()

#     finally:
#         # Commit the changes or rollback if necessary
#         self.commit()

# def create_table(table_name, columns, attributes, drop_if_exists=False):
#     if table_exists(table_name):
#         if drop_if_exists:
#             self.execute(f"DROP TABLE {table_name}")
#         else:
#             return

#     query = f"CREATE TABLE IF NOT EXISTS {table_name} ("

#     for column, attributes in columns.items():
#         query += f"{column} {attributes.upper()}, "

#     query = query.rstrip(", ") + ")"

#     self.execute(query)


def register_user(username, password, role, office):
    # Generate a salt
    salt = get_salt()

    # Hash the password with the salt
    hashed_password = encode(password, salt)

    # # must be unique
    # with fetchall("users", "username", f"username={username}") as exists:
    #     if exists is not None:
    #         return

    # Store the salt, hashed password, and privilege in the database
    query = "INSERT INTO users (username, password, salt, role, office) VALUES (?, ?, ?, ?, ?)"
    commit(query, (username, hashed_password, salt, role, office))
