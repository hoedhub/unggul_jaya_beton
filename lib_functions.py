import sys, os
import hashlib
import random
import string
from datetime import datetime
import lib_globals as gl


def application_path_exec():
    # determine if application is a script file or frozen exe
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(__file__)


def application_path_meipass():
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))


def file_exists(filename):
    res = False
    for root, dirs, files in os.walk(filename):
        for file in files:
            if file == filename:
                res = True
                break
        if res == True:
            break
    return res


def read_file(filename):
    with open(filename, "r") as f:
        return f.read()


def get_dbname():
    # search for config file
    app_path = application_path_exec()
    if not file_exists(gl.config):
        return None
    with open(os.path.join(app_path, gl.config), "r") as config:
        lines = config.readlines()
    for line in lines:
        if "DBNAME" in line:
            db = line[len("DBNAME") :]
            break
    if db is None:
        return None
    return db if file_exists(db) else None


def valid_ext(filename, extension):
    return (
        filename
        if filename.endswith(extension)
        else f'{filename}.{extension.replace(".","")}'
    )


def set_dbname(dbname):
    # search for config file

    app_path = application_path_exec()
    if not file_exists(gl.config):
        with open(gl.config, "w") as config:
            config.write
    with open(os.path.join(app_path, gl.config), "r") as config:
        lines = config.readlines()
    empty = True
    for i, line in enumerate(lines):
        if "DBNAME" in line:
            empty = False
            lines[i] = f"DBNAME={dbname}"
            break
    if empty:
        db = valid_ext(dbname, ".db")
        lines.append(f"DBNAME={db}")

    with open(os.path.join(app_path, gl.config), "w") as config:
        config.writelines(lines)


def get_salt():
    return "".join(random.choices(string.ascii_letters + string.digits, k=8))


def encode(txt, salt):
    return hashlib.sha256((txt + salt).encode()).hexdigest()


def set_date():
    current_timestamp = datetime.now()
    return current_timestamp.strftime("%Y-%m-%d %H:%M:%S")


def get_date(datetime_string):
    dt = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
    timestamp = dt.timestamp()
    return int(timestamp)
