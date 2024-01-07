
import os
from . import requests

SQL_ECHO = False

DIRNAME = os.path.dirname(__file__)
DB_PATH = DIRNAME + '\\data\\mainDatabase.db'
FILESTORAGE_PATH = DIRNAME + '\\data\\file_storage'
PERMFILES_PATH = DIRNAME + '\\data\\permanent_files'

PREPOPULATE = True

DEFAULT_PASSWORD = "d74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1" # = "pass"

PREPOPULATE_USERS = {
    2: requests.User_CreateRequest(handle="test1", visible_name="Amy", email="test1@example.com", password_hash=DEFAULT_PASSWORD),
    3: requests.User_CreateRequest(handle="test2", visible_name="Benjamin", email="test2@example.com", password_hash=DEFAULT_PASSWORD),
    4: requests.User_CreateRequest(handle="test3", visible_name="Connor", email="test3@example.com", password_hash=DEFAULT_PASSWORD),
    5: requests.User_CreateRequest(handle="test4", visible_name="Diana", email="test4@example.com", password_hash=DEFAULT_PASSWORD),
}

PREPOPULATE_GROUPS = {
    1: requests.Group_CreateRequest(title="Testing group 1", owner_id=2)
}