
from pydantic import BaseModel, Field
import os
import secrets
import json
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, JSON, Column, Session, select
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, date
from time import mktime
from ..modules import mod_users as UsersModule
from ..modules import mod_messaging as MessagingModule
from ..modules import exceptions

### Output

class Output_UserEntry(BaseModel):
    user_id: int
    visible_name: str
    handle: str
    can_view: bool
    can_edit: bool

class Output_Subtask(BaseModel):
    id: int
    text: str = Field(nullable=True)
    position: int
    is_done: bool

class Output_Card(BaseModel):
    id: int
    title: str
    description: str = Field(nullable=True)
    column_id: int
    position_y: int
    color: str
    owner: Output_UserEntry
    deadline: int
    users: list[Output_UserEntry]
    subtasks: list[Output_Subtask]

class Output_Column(BaseModel):
    id: int
    board_id: int
    title: str
    position_x: int
    cards: list[Output_Card]
    
class Output_Board(BaseModel):
    id: int
    title: str
    owner: Output_UserEntry
    users: list[Output_UserEntry]
    columns: list[Output_Column]

### SQL & Requests

class Board(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field()
    owner_id: int = Field()
    class Config:
        arbitrary_types_allowed = True

class Board_CreateRequest(BaseModel):
    title: str
    handle: str|None
    owner_id: int

class Column(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    board_id: int = Field()
    title: str = Field()
    position_x: int = Field()

class Column_CreateRequest(BaseModel):
    title: str = Field()
    board_id: int = Field()
    position_x: int = Field()

class Card(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field()
    description: str = Field(nullable=True)
    column_id: int = Field()
    position_y: int = Field()
    color: str = Field()
    owner_id: int = Field()
    deadline: int = Field()

class Card_CreateRequest(BaseModel):
    title: str = Field()
    description: str = Field(nullable=True)
    column_id: int = Field()
    position_y: int = Field()
    color: str = Field()
    owner_id: int = Field()

class AttachedFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    card_id: int = Field()
    file_id: int = Field()

class BoardUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    board_id: int = Field()
    user_id: int = Field()
    can_view: bool = Field()
    can_edit: bool = Field()

class BoardUser_CreateRequest(BaseModel):
    board_id: int
    user_id: int
    can_view: int
    can_edit: int

class CardUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    card_id: int = Field()
    user_id: int = Field()
    can_edit: bool = Field()

class CardUser_CreateRequest(BaseModel):
    card_id: int
    user_id: int
    can_edit: int

class Subtask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field()
    card_id: int = Field()
    position: int = Field()
    is_done: bool = Field()

class Subtask_CreateRequest(BaseModel):
    text: str
    card_id: int
    position: int

### SQL stuff

DIRNAME = os.path.dirname(os.path.dirname(__file__))
DB_USERS_PATH = DIRNAME + '\\data\\db_tasks.db'
print(DB_USERS_PATH)
sqlite_url = f"sqlite:///{DB_USERS_PATH}"
engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)

### Conversion

class Convert:
    @staticmethod
    def userEntry(user: BoardUser|CardUser) -> Output_UserEntry:
        user_list = UsersModule.select_users(UsersModule.User.id == user.user_id)
        user_publicInfo = UsersModule.convertUserToPublic(user_list[0])
        return Output_UserEntry(
            user_id=user.user_id, visible_name=user_publicInfo.visible_name, handle=user_publicInfo.handle, 
            can_view=user.can_view, can_edit=user.can_edit)
    @staticmethod
    def subtask(subtask: Subtask) -> Output_Subtask:
        return Output_Subtask(**subtask.__dict__)
    @staticmethod
    def card(card: Card) -> Output_Card:
        res = Output_Card(**card.__dict__)
        res.subtasks = list(map(Convert.subtask, Select.subtasks(Subtask.card_id == card.id)))
        res.users = list(map(Convert.userEntry, Select.cardUsers(CardUser.card_id == card.id)))
        res.owner = Convert.userEntry(Select.oneCardUser(CardUser.card_id == card.id, CardUser.user_id == card.owner_id))
        return res
    @staticmethod
    def column(column: Column) -> Output_Column:
        res = Output_Column(**column.__dict__)
        res.cards = list(map(Convert.card, Select.cards(Card.column_id == column.id)))
        return res
    @staticmethod
    def board(board: Board) -> Output_Board:
        res = Output_Card(**board.__dict__)
        res.columns = list(map(Convert.card, Select.columns(Column.board_id == board.id)))
        res.users = list(map(Convert.userEntry, Select.boardUsers(BoardUser.card_id == board.id)))
        res.owner = Convert.userEntry(Select.oneBoardUser(BoardUser.board_id == board.id, BoardUser.user_id == board.owner_id))
        return res

### Create

class Create:
    @staticmethod
    def board(request: Board_CreateRequest) -> Board:
        boardToCreate = Board(title=request.title, owner_id=request.owner_id)
        print(boardToCreate)
        with Session(engine) as session:
            session.add(boardToCreate)
            session.commit()
            session.refresh(boardToCreate)

            Create.boardUser(BoardUser_CreateRequest(user_id=request.owner_id, board_id=boardToCreate.id, can_edit=True, can_view=True))

            return boardToCreate
    @staticmethod
    def column(request: Column_CreateRequest) -> Column:
        with Session(engine) as session:
            columnToCreate = Column(board_id=request.board_id, title=request.title, position_x=request.position_x)
            print(columnToCreate)
            session.add(columnToCreate)
            session.commit()
            session.refresh(columnToCreate)
            return columnToCreate
    @staticmethod
    def card(request: Card_CreateRequest) -> Card:
        with Session(engine) as session:
            boardUser = Select.oneBoardUser(BoardUser.user_id==request.owner_id, BoardUser.board_id==request.board_id)
            if (boardUser == None):
                raise Exception()
            toCreate = Column(board_id=request.board_id, title=request.title, position_x=request.position_x)
            print(toCreate)
            session.add(toCreate)
            session.commit()
            session.refresh(toCreate)
            return toCreate
    @staticmethod
    def subtask(request: Subtask_CreateRequest) -> Subtask:
        with Session(engine) as session:
            toCreate = Subtask(text=request.text, card_id=request.card_id, position=request.position, is_done=False)
            session.add(toCreate)
            session.commit()
            session.refresh(toCreate)
            return toCreate
    @staticmethod
    def boardUser(request: BoardUser_CreateRequest) -> BoardUser:
        with Session(engine) as session:
            toCreate = BoardUser(board_id=request.board_id, user_id=request.user_id, can_edit=request.can_edit, can_view=request.can_view)
            print(toCreate)
            session.add(toCreate)
            session.commit()
            session.refresh(toCreate)
            return toCreate
    @staticmethod
    def cardUser(request: CardUser_CreateRequest) -> BoardUser:
        with Session(engine) as session:
            toCreate = CardUser(card_id=request.card_id, user_id=request.user_id, can_edit=request.can_edit)
            print(toCreate)
            session.add(toCreate)
            session.commit()
            session.refresh(toCreate)
            return toCreate

### Select

class Select:
    ### Select # Raw
    @staticmethod
    def __select(targetType, *expressions) -> list:
        with Session(engine) as session:
            statement = select(targetType)
            if len(expressions) != 0:
                statement = statement.where(*expressions)
            results = session.exec(statement)
            result_list = results.all()
            print("Select:")
            print(result_list)
            return result_list
    @staticmethod
    def __select_one(targetType, *expressions):
        with Session(engine) as session:
            statement = select(targetType)
            if len(expressions) != 0:
                statement = statement.where(*expressions)
            results = session.exec(statement)
            return results.one()

    ### Select # Output_*
    @staticmethod
    def boards(*expressions) -> list[Output_Board]:
        return list(map(Convert.board, Select.__select(Board, *expressions)))
        select_list = Select.__select_boards(*expressions)
        result_list = []
        for i in select_list:
            newObject = Convert.board(i)
            newObject.owner = Select.boardUsers(BoardUser.user_id == i.owner_id, BoardUser.board_id == i.id)[0]
            newObject.users = Select.boardUsers(BoardUser.board_id == i.id)
            result_list.append(newObject)
        return result_list
    @staticmethod
    def columns(*expressions) -> list[Output_Column]:
        return list(map(Convert.column, Select.__select(Columns, *expressions)))
        result_list = list(map(Convert.column, Select.__select_columns(*expressions)))
        for i in result_list: i.cards = Select.cards(Card.column_id == i.id)
        return result_list
    @staticmethod
    def cards(*expressions) -> list[Output_Card]:
        return list(map(Convert.card, Select.__select(Card, *expressions)))
        select_list = Select.__select_cards(*expressions)
        result_list = []
        for i in select_list:
            newObject = Convert.board(i)
            newObject.subtasks = Select.subtasks(Subtask.card_id == i.id)
            newObject.owner = Select.boardUsers(BoardUser.board_id == i.id, BoardUser.user_id == i.owner_id)[0]
            newObject.users = Select.boardUsers(BoardUser.board_id == i.id)
            result_list.append(newObject)
        return result_list
    @staticmethod
    def subtasks(*expressions) -> list[Output_Subtask]:
        return list(map(Convert.subtask, Select.__select(Subtask, *expressions)))
    @staticmethod
    def cardUsers(*expressions) -> list[Output_UserEntry]:
        return list(map(Convert.userEntry, Select.__select(CardUser, *expressions)))
    @staticmethod
    def boardUsers(*expressions) -> list[Output_UserEntry]:
        return list(map(Convert.userEntry, Select.__select(BoardUser, *expressions)))

    ### Select # One
    @staticmethod
    def __select_one(select_list: list, conversion_method):
        if len(select_list) == 1: return conversion_method(select_list[0])
        else: raise exceptions.MoreThanOneOrZeroException()
    @staticmethod
    def oneBoard(*expressions) -> Output_Board:
        return Select.__select_one(Select.__select(*expressions), Convert.board)
    @staticmethod
    def oneColumn(*expressions) -> Output_Column:
        return Select.__select_one(Select.__select(*expressions), Convert.board)
    @staticmethod
    def oneCard(*expressions) -> Output_Card:
        return Select.__select_one(Select.__select(*expressions), Convert.board)
    @staticmethod
    def oneSubtask(*expressions) -> Output_Subtask:
        return Select.__select_one(Select.__select(*expressions), Convert.board)
    @staticmethod
    def oneBoardUser(*expressions) -> Output_UserEntry:
        return Select.__select_one(Select.__select(*expressions), Convert.board)
    @staticmethod
    def oneCardUser(*expressions) -> Output_UserEntry:
        return Select.__select_one(Select.__select(*expressions), Convert.board)

    ### Select # Special
    @staticmethod
    def boardsOfUser(user_id: int) -> list[Output_Board]:
        board_user_list = Select.__select(BoardUser, BoardUser.user_id == user_id)
        result_list = []
        for i in board_user_list:
            try:
                board = Select.oneBoard(Board.id == i.board_id)
            except:
                print(f"Board with id {i.board_id} doesn't exist")
                continue
            result_list.append(board)
        return result_list
            
### List
class List:
    @staticmethod
    def boards() -> list[Output_Board]:
        return Select.boards()
    @staticmethod
    def columns() -> list[Output_Column]:
        return Select.columns()
    @staticmethod
    def cards() -> list[Output_Card]:
        return Select.cards()
    @staticmethod
    def subtasks() -> list[Output_Subtask]:
        return Select.subtasks()
    @staticmethod
    def boardUsers() -> list[Output_UserEntry]:
        return Select.boardUsers()
    @staticmethod
    def cardUsers() -> list[Output_UserEntry]:
        return Select.cardUsers()
