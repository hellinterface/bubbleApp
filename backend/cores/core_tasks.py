
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, JSON, Column, Session, select
from datetime import datetime, timedelta, date
from time import mktime

from .. import exceptions
from .. import config
from ..models import Output_TasksUserEntry, Output_Subtask, Output_Card, Output_Column, Output_Board, Output_TasksGroupEntry, Output_File
from ..requests import Card_CreateRequest, Card_UpdateRequest, Board_CreateRequest, Board_UpdateRequest
from ..requests import Column_CreateRequest, Column_UpdateRequest, Subtask_CreateRequest, Subtask_UpdateRequest
from ..requests import BoardGroup_UpdateRequest, BoardGroup_CreateRequest, BoardUser_CreateRequest, BoardUser_UpdateRequest
from ..requests import CardUser_CreateRequest, CardUser_UpdateRequest

###
###   Entites :: Output
###

class Board(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field()
    owner_id: int = Field()
    class Config:
        arbitrary_types_allowed = True

class Column(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    board_id: int = Field()
    title: str = Field()
    position_x: int = Field()

class Card(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field()
    description: str = Field(nullable=True)
    column_id: int = Field()
    position_y: int = Field()
    color: str = Field()
    owner_id: int = Field()
    deadline: Optional[int] = Field()

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

class BoardGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    board_id: int = Field()
    group_id: int = Field()
    can_view: bool = Field()
    can_edit: bool = Field()

class CardUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    card_id: int = Field()
    user_id: int = Field()
    can_edit: bool = Field()

class Subtask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field()
    card_id: int = Field()
    position: int = Field()
    is_done: bool = Field()

###
###   SQL Database Engine
###

sqlite_url = f"sqlite:///{config.DB_PATH}"
engine = create_engine(sqlite_url, echo=config.SQL_ECHO)
SQLModel.metadata.create_all(engine)

###
###   Data :: Convert
###

class Convert:
    @staticmethod
    def userEntry(user: BoardUser|CardUser) -> Output_TasksUserEntry:
        from ..cores import core_users as UsersModule
        userInfo = UsersModule.RawSelect.oneUser(UsersModule.User.id == user.user_id)
        user_publicInfo = UsersModule.Convert.userToPublic(userInfo)
        return Output_TasksUserEntry(user_information=user_publicInfo, can_view=True, can_edit=user.can_edit)
    @staticmethod
    def groupEntry(group: BoardGroup) -> Output_TasksGroupEntry:
        from ..cores import core_groups as GroupsModule
        groupInfo = GroupsModule.Select.oneGroup(GroupsModule.Group.id == group.group_id)
        return Output_TasksUserEntry(user_information=groupInfo, can_view=group.can_view, can_edit=group.can_edit)
    @staticmethod
    def subtask(subtask: Subtask) -> Output_Subtask:
        return Output_Subtask(**subtask.__dict__)
    @staticmethod
    def card(card: Card) -> Output_Card:
        res = Output_Card(
            **card.__dict__,
            subtasks = Select.subtasks(Subtask.card_id == card.id),
            users = Select.cardUsers(CardUser.card_id == card.id),
            owner = Select.oneCardUser(CardUser.card_id == card.id, CardUser.user_id == card.owner_id)
        )
        return res
    @staticmethod
    def column(column: Column) -> Output_Column:
        res = Output_Column(
            **column.__dict__,
            cards = Select.cards(Card.column_id == column.id)
        )
        return res
    @staticmethod
    def board(board: Board) -> Output_Board:
        res = Output_Board(
            **board.__dict__,
            columns = Select.columns(Column.board_id == board.id),
            users = Select.boardUsers(BoardUser.board_id == board.id),
            groups = Select.boardGroups(BoardGroup.board_id == board.id),
            owner = Select.oneBoardUser(BoardUser.board_id == board.id, BoardUser.user_id == board.owner_id)
        )
        return res
    @staticmethod
    def attachedFile(attachedFile: AttachedFile) -> Output_File:
        from ..cores import core_files as FilesModule
        return FilesModule.Select.oneFile(FilesModule.File.id == attachedFile.file_id)

###
###   Data :: Create
###

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
            column = RawSelect.oneColumn(Column.id == request.column_id)
            # Проверка на наличие указанного пользователя в списке пользователей доски
            boardUser = Select.oneBoardUser(BoardUser.user_id==request.owner_id, BoardUser.board_id==column.board_id)
            if (boardUser == None):
                raise Exception()
            toCreate = Card(title=request.title, description=request.description, column_id=request.column_id, position_y=request.position_y, color=request.color, owner_id=request.owner_id, deadline=None)
            print(toCreate)
            session.add(toCreate)
            session.commit()
            session.refresh(toCreate)

            Create.cardUser(CardUser_CreateRequest(user_id=request.owner_id, card_id=toCreate.id, can_edit=True, can_view=True))

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
    def boardGroup(request: BoardGroup_CreateRequest) -> BoardGroup:
        with Session(engine) as session:
            toCreate = BoardGroup(board_id=request.board_id, group_id=request.group_id, can_edit=request.can_edit, can_view=request.can_view)
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

###
###   Data :: Raw Select
###

class RawSelect:
    @staticmethod
    def select(targetType, *expressions) -> list:
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
    def select_one(targetType, *expressions):
        with Session(engine) as session:
            statement = select(targetType)
            if len(expressions) != 0:
                statement = statement.where(*expressions)
            results = session.exec(statement)
            return results.one_or_none()
    @staticmethod
    def boards(*expressions) -> list[Board]:
        return RawSelect.select(Board, *expressions)
    @staticmethod
    def columns(*expressions) -> list[Column]:
        return RawSelect.select(Column, *expressions)
    @staticmethod
    def cards(*expressions) -> list[Card]:
        return RawSelect.select(Card, *expressions)
    @staticmethod
    def subtasks(*expressions) -> list[Subtask]:
        return RawSelect.select(Subtask, *expressions)
    @staticmethod
    def boardUsers(*expressions) -> list[BoardUser]:
        return RawSelect.select(BoardUser, *expressions)
    @staticmethod
    def boardGroups(*expressions) -> list[BoardGroup]:
        return RawSelect.select(BoardGroup, *expressions)
    @staticmethod
    def cardUsers(*expressions) -> list[CardUser]:
        return RawSelect.select(CardUser, *expressions)
        
    @staticmethod
    def oneBoard(*expressions) -> Board:
        return RawSelect.select_one(Board, *expressions)
    @staticmethod
    def oneColumn(*expressions) -> Column:
        return RawSelect.select_one(Column, *expressions)
    @staticmethod
    def oneCard(*expressions) -> Card:
        return RawSelect.select_one(Card, *expressions)
    @staticmethod
    def oneSubtask(*expressions) -> Subtask:
        return RawSelect.select_one(Subtask, *expressions)
    @staticmethod
    def oneBoardUser(*expressions) -> BoardUser:
        return RawSelect.select_one(BoardUser, *expressions)
    @staticmethod
    def oneBoardGroup(*expressions) -> BoardGroup:
        return RawSelect.select_one(BoardGroup, *expressions)
    @staticmethod
    def oneCardUser(*expressions) -> CardUser:
        return RawSelect.select_one(CardUser, *expressions)

###
###   Data :: Select
###

class Select:
    @staticmethod
    def boards(*expressions) -> list[Output_Board]:
        return list(map(Convert.board, RawSelect.select(Board, *expressions)))
    @staticmethod
    def columns(*expressions) -> list[Output_Column]:
        return list(map(Convert.column, RawSelect.select(Column, *expressions)))
    @staticmethod
    def cards(*expressions) -> list[Output_Card]:
        return list(map(Convert.card, RawSelect.select(Card, *expressions)))
    @staticmethod
    def subtasks(*expressions) -> list[Output_Subtask]:
        return list(map(Convert.subtask, RawSelect.select(Subtask, *expressions)))
    @staticmethod
    def cardUsers(*expressions) -> list[Output_TasksUserEntry]:
        return list(map(Convert.userEntry, RawSelect.select(CardUser, *expressions)))
    @staticmethod
    def boardUsers(*expressions) -> list[Output_TasksUserEntry]:
        return list(map(Convert.userEntry, RawSelect.select(BoardUser, *expressions)))
    @staticmethod
    def boardGroups(*expressions) -> list[Output_TasksGroupEntry]:
        return list(map(Convert.groupEntry, RawSelect.select(BoardGroup, *expressions)))

    ### Select # One
    @staticmethod
    def oneBoard(*expressions) -> Output_Board:
        return Convert.board(RawSelect.select_one(Board, *expressions))
    @staticmethod
    def oneColumn(*expressions) -> Output_Column:
        return Convert.column(RawSelect.select_one(Column, *expressions))
    @staticmethod
    def oneCard(*expressions) -> Output_Card:
        return Convert.card(RawSelect.select_one(Card, *expressions))
    @staticmethod
    def oneSubtask(*expressions) -> Output_Subtask:
        return Convert.subtask(RawSelect.select_one(Subtask, *expressions))
    @staticmethod
    def oneCardUser(*expressions) -> Output_TasksUserEntry:
        return Convert.userEntry(RawSelect.select_one(CardUser, *expressions))
    @staticmethod
    def oneBoardUser(*expressions) -> Output_TasksUserEntry:
        return Convert.userEntry(RawSelect.select_one(BoardUser, *expressions))
    @staticmethod
    def oneBoardGroup(*expressions) -> Output_TasksGroupEntry:
        return Convert.groupEntry(RawSelect.select_one(BoardGroup, *expressions))

    ### Select # Special
    @staticmethod
    def boardsOfUser(user_id: int) -> list[Output_Board]:
        board_user_list = RawSelect.select(BoardUser, BoardUser.user_id == user_id)
        result_list = []
        for i in board_user_list:
            try:
                board = Select.oneBoard(Board.id == i.board_id)
            except:
                print(f"Board with id {i.board_id} doesn't exist")
                continue
            result_list.append(board)
        return result_list
    @staticmethod
    def boardsOfGroup(group_id: int) -> list[Output_Board]:
        board_group_list = RawSelect.select(BoardGroup, BoardGroup.group_id == group_id)
        result_list = []
        for i in board_group_list:
            try:
                board = Select.oneBoard(Board.id == i.board_id)
            except:
                print(f"Board with id {i.board_id} doesn't exist")
                continue
            result_list.append(board)
        return result_list
            
###
###   Data :: List
###

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
    def cardUsers() -> list[Output_TasksUserEntry]:
        return Select.cardUsers()
    @staticmethod
    def boardUsers() -> list[Output_TasksUserEntry]:
        return Select.boardUsers()
    @staticmethod
    def boardGroups() -> list[Output_TasksGroupEntry]:
        return Select.boardGroups()


###
###   Data :: Update
###

class Update:
    @staticmethod
    def board(request: Board_UpdateRequest) -> Board:
        target = RawSelect.oneBoard(Board.id == request.id)
        for (key, value) in iter(request):
            if (value != None):
                print(key, value)
                setattr(target, key, value)
        print(target)
        with Session(engine) as session:
            session.add(target)
            session.commit()
            session.refresh(target)
            return target
    @staticmethod
    def column(request: Column_UpdateRequest) -> Column:
        debugPrefix = "TASKS :: Updating column ::"
        print(f"{debugPrefix} Request:")
        print(Column_UpdateRequest)
        target = RawSelect.oneColumn(Column.id == request.id)
        for (key, value) in iter(request):
            if (value != None):
                print(key, value)
                setattr(target, key, value)
        print(f"{debugPrefix} Updating to:")
        print(target)
        with Session(engine) as session:
            session.add(target)
            session.commit()
            session.refresh(target)
            return target
    @staticmethod
    def card(request: Card_UpdateRequest) -> Card:
        target = RawSelect.oneCard(Card.id == request.id)
        for (key, value) in iter(request):
            if (value != None):
                if (key == "attached_files"):
                    RawSelect.attachedFile(AttachedFile.card_id)
                    continue
                print(key, value)
                setattr(target, key, value)
        print(target)
        with Session(engine) as session:
            session.add(target)
            session.commit()
            session.refresh(target)
            return target
    @staticmethod
    def subtask(request: Subtask_UpdateRequest) -> Subtask:
        target = RawSelect.oneSubtask(Subtask.id == request.id)
        for (key, value) in iter(request):
            if (value != None):
                print(key, value)
                setattr(target, key, value)
        print(target)
        with Session(engine) as session:
            session.add(target)
            session.commit()
            session.refresh(target)
            return target
    @staticmethod
    def cardUser(request: CardUser_UpdateRequest) -> CardUser:
        target = RawSelect.oneCardUser(CardUser.card_id == request.card_id, CardUser.user_id == request.user_id)
        for (key, value) in iter(request):
            if (value != None):
                print(key, value)
                setattr(target, key, value)
        print(target)
        with Session(engine) as session:
            session.add(target)
            session.commit()
            session.refresh(target)
            return target
    @staticmethod
    def boardUser(request: BoardUser_UpdateRequest) -> BoardUser:
        target = RawSelect.oneBoardUser(BoardUser.board_id == request.board_id, CardUser.user_id == request.user_id)
        for (key, value) in iter(request):
            if (value != None):
                print(key, value)
                setattr(target, key, value)
        print(target)
        with Session(engine) as session:
            session.add(target)
            session.commit()
            session.refresh(target)
            return target
    @staticmethod
    def boardGroup(request: BoardGroup_UpdateRequest) -> BoardGroup:
        target = RawSelect.oneBoardGroup(BoardGroup.board_id == request.board_id, BoardGroup.group_id == request.group_id)
        for (key, value) in iter(request):
            if (value != None):
                print(key, value)
                setattr(target, key, value)
        print(target)
        with Session(engine) as session:
            session.add(target)
            session.commit()
            session.refresh(target)
            return target

###
###   Data :: Delete
###

class Delete:
    @staticmethod
    def board(target_id: int) -> Board:
        board = RawSelect.select_one(Board, Board.id == target_id)
        if (board != None):
            with Session(engine) as session:
                session.delete(board)  
                session.commit()
                # Delete boardUsers
                for i in RawSelect.select(BoardUser, BoardUser.board_id == target_id):
                    Delete.boardUser(i.id)
                # Delete columns
                for i in RawSelect.select(Column, Column.board_id == target_id):
                    Delete.column(i.id)
                return board
        else:
            raise Exception()
    @staticmethod
    def column(target_id: int) -> Column:
        column = RawSelect.select_one(Column, Column.id == target_id)
        if (column != None):
            with Session(engine) as session:
                session.delete(column)  
                session.commit()
                # Delete cards
                for i in RawSelect.select(Card, Card.column_id == target_id):
                    Delete.card(i.id)
                return column
        else:
            raise Exception()
    @staticmethod
    def card(target_id: int) -> Card:
        card = RawSelect.select_one(Card, Card.id == target_id)
        if (card != None):
            with Session(engine) as session:
                session.delete(card)  
                session.commit()
                # Delete cardUsers
                for i in RawSelect.select(CardUser, CardUser.card_id == target_id):
                    Delete.cardUser(i.id)
                # Delete subtasks
                for i in RawSelect.select(Subtask, Subtask.card_id == target_id):
                    Delete.subtask(i.id)
                return card
        else:
            raise Exception()
    @staticmethod
    def subtask(target_id: int) -> Subtask:
        subtask = RawSelect.select_one(Subtask, Subtask.id == target_id)
        if (subtask != None):
            with Session(engine) as session:
                session.delete(subtask)  
                session.commit()  
                return subtask
        else:
            raise Exception()
    @staticmethod
    def boardGroup(group_id: int, board_id: int) -> BoardGroup:
        group = RawSelect.select_one(BoardGroup, BoardGroup.board_id == board_id, BoardGroup.group_id == group_id)
        if (group != None):
            with Session(engine) as session:
                session.delete(group)  
                session.commit()  
                return group
        else:
            raise Exception()
    @staticmethod
    def boardUser(user_id: int, board_id: int) -> BoardUser:
        user = RawSelect.select_one(BoardUser, BoardUser.board_id == board_id, BoardUser.user_id == user_id)
        if (user != None):
            with Session(engine) as session:
                session.delete(user)  
                session.commit()  
                return user
        else:
            raise Exception()
    @staticmethod
    def cardUser(user_id: int, card_id: int) -> CardUser:
        user = RawSelect.select_one(CardUser, CardUser.card_id == card_id, CardUser.user_id == user_id)
        if (user != None):
            with Session(engine) as session:
                session.delete(user)  
                session.commit()  
                return user
        else:
            raise Exception()
    @staticmethod
    def attachedFile(target_id: int) -> AttachedFile:
        attachedFile = RawSelect.select_one(AttachedFile, AttachedFile.id == target_id)
        if (attachedFile != None):
            with Session(engine) as session:
                session.delete(attachedFile)
                session.commit()
                return attachedFile
        else:
            raise Exception()

