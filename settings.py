import os
import pathlib
import datetime

HOST = "localhost"
PORT = 8080

STORAGE_ROOT = os.path.joint(pathlib.Path(__file__).resolve().parent, "storage")
DATABASE_ROOT = os.path.joint(pathlib.Path(__file__).resolve().parent, "database")

ADMIN_USERNAME = "sonagraduation"
ADMIN_DOB = datetime.date(2024, 1, 1)

os.makedirs(STORAGE_ROOT, exist_ok=True)
os.makedirs(DATABASE_ROOT, exist_ok=True)
