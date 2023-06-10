import sqlite3
import os
from lib_functions import encode, get_salt
from lib_globals import dbname


def setup_db():
    if os.path.exists(dbname):
        return
    try:
        connection = sqlite3.connect(dbname)
        cursor = connection.cursor()
        # incommit
        cursor.execute(
            """
CREATE TABLE IF NOT EXISTS incommit(
    incommit_id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER,
    query TEXT,
    timestamp TEXT,
    executed INTEGER);
    """
        )
        connection.commit()
        print('table "incommit" created')

        # excommit
        cursor.execute(
            """
CREATE TABLE IF NOT EXISTS excommit(
    excommit_id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER,
    query TEXT,
    timestamp TEXT,
    executed INTEGER);
    """
        )
        connection.commit()
        print('table "excommit" created')

        # users
        cursor.execute(
            """
CREATE TABLE IF NOT EXISTS users(
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    salt TEXT NOT NULL,
    role TEXT NOT NULL,
    office TEXT);
    """
        )  # office_id TEXT karena satu user bisa banya office_id tupple/list
        connection.commit()
        print('table "users" created')

        # Harus ada user awal sbg developer
        salt = get_salt()
        password = encode("123", salt)
        cursor.execute(
            "INSERT INTO users(username, password, salt, role, office) VALUES(?, ?, ?, ?, ?);",
            ("ujb", password, salt, "developer", ""),
        )
        connection.commit()
        print('table "users" updated')

        # roles = ('developer', 'manager', 'admin', 'operator')
        cursor.execute("CREATE TABLE IF NOT EXISTS roles(role UNIQUE NOT NULL);")
        connection.commit()
        print('table "roles" created')

        roles = [("developer",), ("manager",), ("admin",), ("operator",)]
        cursor.executemany(f"INSERT INTO roles(role) VALUES(?);", roles)
        connection.commit()
        print('table "roles" updated')

        # offices
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS offices(name TEXT UNIQUE NOT NULL, address TEXT);"
        )
        connection.commit()
        print('table "offices" created')

        # pembelian
        cursor.execute(
            """
CREATE TABLE IF NOT EXISTS pembelian(
    pembelian_id INTEGER PRIMARY KEY NOT NULL,
    kwitansi TEXT,
    tanggal TEXT NOT NULL,
    stok_id INTEGER,
    qty INTEGER,
    harga REAL,
    jumlah REAL);
"""
        )
        connection.commit()
        print('table "pembelian" created')

        # penggunaan
        cursor.execute(
            """
CREATE TABLE IF NOT EXISTS penggunaan(
    penggunaan_id INTEGER PRIMARY KEY NOT NULL,
    tanggal TEXT,
    pembelian_id INTEGER,
    qty INTEGER,
    pengguna TEXT UNIQUE NOT NULL,
    request INTEGER);
"""
        )
        connection.commit()
        print('table "penggunaan" created')

        # pengguna
        cursor.execute(
            """
CREATE TABLE IF NOT EXISTS pengguna(
    pengguna TEXT UNIQUE NOT NULL,
    lambung TEXT);
"""
        )
        connection.commit()
        print('table "pengguna" created')

        # barang
        cursor.execute(
            """
CREATE TABLE IF NOT EXISTS stok(
    deskripsi TEXT UNIQUE NOT NULL,
    part TEXT,
    asal TEXT,
    qty INTEGER,
    satuan TEXT,
    stok INTEGER);
"""
        )
        connection.commit()
        print('table "stok" created')

        # satuan
        cursor.execute(
            """
CREATE TABLE IF NOT EXISTS satuan(
    satuan TEXT UNIQUE NOT NULL);
"""
        )
        connection.commit()
        print('table "satuan" created')
        connection.close()
    except Exception as e:
        print("Setup DB failed: ", str(e))
        connection.close()
