
import sqlite3
from pydantic import BaseModel, Field

class InvalidDatabaseException(Exception):
    def __init__(self):
        pass

class BData:
    def __init__(self, path, row_factory):
        self.path = path
        self.row_factory = row_factory
        pass

    def __check(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        tables = conn.execute("SELECT * FROM sqlite_master WHERE type='table'").fetchall()
        if len(tables) == 0:
            return False
        else:
            return True

    def create(self, table_name, model):
        primary_key = None
        array = []
        for key, value in model.__dict__["model_fields"].items():
            temp_string = f'"{key}"'
            if (value.json_schema_extra == None):
                value.json_schema_extra = dict()
            if (value.json_schema_extra.get("bdata_type") == str):
                temp_string += " INTEGER"
            else:
                temp_string += " TEXT"
            if (value.json_schema_extra.get("dbata_can_be_null") != True):
                temp_string += " NOT NULL"
            if (value.json_schema_extra.get("bdata_unique") == True):
                temp_string += " UNIQUE"
            if (value.json_schema_extra.get("dbata_primary") == True or primary_key == None):
                primary_key = key
            array.append(temp_string)
        query = f'''CREATE TABLE "{table_name}" ({",".join(array)},PRIMARY KEY("{primary_key}"));'''
        print(query)
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute(query)
        conn.close()
        print("******* database created. *******")

    def __connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = self.row_factory
        # if not self.__check(): create(conn)
        return conn

    def select(self, table_name: str, request: list|dict|str|None = None):
        """
            Возвращает из указанной таблицы базы данных все строки, которые соответствуют
            приведённому запросу request, который может быть представлен тремя типами:
            1. Если request - это строка '*', то возвращаются все строки из таблицы.
            2. Если request - это словарь, то всё в нём объединяется операцией AND.
            3. Если request - это список, то он может содержать списки и словари.
            Словари объединяют всё, что в них есть, операцией AND, а списки - OR.
            В случае, если в словаре ключу соответсвует список, то все элементы списка объединяются операцией AND.
            Также, если в словаре перед ключом стоит восклицательный знак (например, "!id"), то накладывается операция NOT.

            Пример 1: если request выглядит так:
            { "user_id": "111", handle: "test" },
            то совершится запрос с поиском (user_id=111 AND handle=test).

            Пример 2: если request выглядит так:
            [
                {
                    "join_date": ["1970", "2020"],
                    "!is_admin": 1
                },
                [
                    {"user_id": "222"},
                    {"user_id": "333"},
                    {"handle": "test"},
                    {
                        "user_id": "444",
                        "handle": "some"
                    }
                ]
            ],
            то совершится запрос с поиском (join_date=1970 AND join_date=2020 AND NOT is_admin=1) OR (user_id=222 OR user_id=333 OR handle=test OR (user_id=444 AND handle=some)).
        """
        """request = [
            {
                "user_id": ["111111", "222222"],
                "!is_admin": 0
            },
            [
                {"user_id": "333"},
                {"handle": "test"}
            ]
        ]"""
        string = f"SELECT * FROM {table_name}"
        if (request == None):
            raise Exception
        elif isinstance(request, str):
            print("REQUEST:" + request)
            if (request != "*"):
                raise Exception
        else:
            string += " WHERE "
            string += self.__MAKE_WHERE(request)
        print(string)
        dbc = self.__connect()
        return dbc.execute(string).fetchall()

    def __MAKE_WHERE(self, request: list|dict|None = None):
        if (request == None):
            raise Exception
        string = ""
        if isinstance(request, dict):
            string = self.__JOIN_AND(request)
        elif isinstance(request, list):
            string = self.__JOIN_OR(request)
        return string 

    def __JOIN_AND(self, entry: dict):
        array = []
        for key in entry.keys():
            string = ""
            value = entry[key]
            if isinstance(value, list):
                temp_string = f'''"{f'" AND {key}="'.join(value)}"'''
            else:
                temp_string = f'"{value}"'
            string += f"({key}={temp_string})"
            array.append(string)
        return f'''({" AND ".join(array)})'''

    def __JOIN_OR(self, entry: list):
        array = []
        for i in entry:
            if isinstance(i, list):
                array.append(self.__JOIN_OR(i))
            elif isinstance(i, dict):
                array.append(self.__JOIN_AND(i))
        return f'''({" OR ".join(array)})'''
        
    def replaceNoneWithEmptyString(self, x):
        if x == None:
            return ""
        else:
            return x

    def insert(self, table_name, dictionary: BaseModel):
        #dbc = self.__connect()
        #cur = dbc.cursor()
        dictionary = dictionary.model_dump()
        values = list(map(self.replaceNoneWithEmptyString, dictionary.values()))
        for i in values:
            if i == None:
                i = ""
        values = list(map(str, values))
        query = f'''INSERT INTO {table_name} ({','.join(dictionary.keys())}) VALUES ("{'","'.join(values)}")'''
        print(query)
        #dbc.commit()

# position 0 = default profile
class UserProfile(BaseModel):
    position: int
    title: str
    visible_name: str
    avatar_fileid: str | None = None
    bio: str
    contacts: list[str]
    groups: list[str]
    notifications: list[str]
    events: list[str]

class User(BaseModel):
    id: str = Field(allow_mutation=False, bdata_unique=True)
    handle: str = Field(bdata_unique=True)
    visible_name: str = Field()
    email: str = Field(bdata_unique=True)
    password_hash: str = Field()
    join_date: int = Field()
    profiles: list[UserProfile] = Field(bdata_type=str)
    folder_id: str = Field(bdata_unique=True)

#bd = BData("test_bdata.db", sqlite3.Row)
#bd.create("Users", User)
#bd.select("Users", {"user_id": 14515})