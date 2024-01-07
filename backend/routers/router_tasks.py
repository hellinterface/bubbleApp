

from fastapi import APIRouter, Depends, Request, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from ..cores import core_users as UsersModule
from ..cores import core_tasks as TasksModule

###
###   Routers
###

router = APIRouter(
    prefix="/api/tasks",
    tags=["Tasks"],
    dependencies=[Depends(UsersModule.get_token_header)],
    responses={404: {"description": "Not found"}},
)

router_ws = APIRouter(
    prefix="/api/tasks",
    tags=["Tasks"],
    responses={404: {"description": "Not found"}},
)

###
###   Requests :: Create
###

class RouterRequest_CreateBoard(BaseModel):
    title: str

class RouterRequest_CreateColumn(BaseModel):
    title: str
    board_id: int
    position_x: int

class RouterRequest_CreateCard(BaseModel):
    title: str
    description: str
    column_id: int
    position_y: int
    color: str = Field(default="#579")

class RouterRequest_CreateSubtask(BaseModel):
    text: str
    card_id: int
    position: int

###
###   Requests :: Update
###

class RouterRequest_UpdateBoard(BaseModel):
    id: int
    title: Optional[str]
    owner_id: Optional[int]

class RouterRequest_UpdateColumn(BaseModel):
    id: int
    board_id: Optional[int]
    title: Optional[str]
    position_x: Optional[int]

class RouterRequest_UpdateCard(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    column_id: Optional[int]
    position_y: Optional[int]
    color: Optional[str]
    owner_id: Optional[int]
    deadline: Optional[int]
    attached_files: Optional[list[int]]

class RouterRequest_UpdateSubtask(BaseModel):
    id: int
    text: Optional[str]
    card_id: Optional[int]
    position: Optional[int]
    is_done: Optional[bool]

class RouterRequest_UpdateBoardUser(BaseModel):
    board_id: int
    user_id: int
    can_view: Optional[bool]
    can_edit: Optional[bool]

class RouterRequest_UpdateBoardGroup(BaseModel):
    board_id: int
    group_id: int
    can_view: Optional[bool]
    can_edit: Optional[bool]

class RouterRequest_UpdateCardUser(BaseModel):
    card_id: int
    user_id: int
    can_edit: Optional[bool]

###
###   Endpoints :: Create
###

@router.post("/createBoard", response_class=JSONResponse, response_model=TasksModule.Output_Board)
async def post_create_board(createRequest: RouterRequest_CreateBoard, req: Request):
    print(createRequest.__dict__)
    newBoard = TasksModule.Create.board(
        TasksModule.Board_CreateRequest(**createRequest.__dict__, owner_id=req.state.current_user.id)
    )
    return TasksModule.Convert.board(newBoard)

@router.post("/createColumn", response_class=JSONResponse, response_model=TasksModule.Output_Column)
async def post_create_column(createRequest: RouterRequest_CreateColumn, req: Request):
    print(createRequest.__dict__)
    newColumn = TasksModule.Create.column(
        TasksModule.Column_CreateRequest(**createRequest.__dict__)
    )
    await websocket_broadcast_update(newColumn.board_id)
    return TasksModule.Convert.column(newColumn)

@router.post("/createCard", response_class=JSONResponse, response_model=TasksModule.Output_Card)
async def post_create_card(createRequest: RouterRequest_CreateCard, req: Request):
    print(createRequest.__dict__)
    newCard = TasksModule.Create.card(
        TasksModule.Card_CreateRequest(**createRequest.__dict__, owner_id=req.state.current_user.id)
    )
    column = TasksModule.RawSelect.oneColumn(TasksModule.Column.id == newCard.column_id)
    await websocket_broadcast_update(column.board_id)
    return TasksModule.Convert.card(newCard)

@router.post("/createSubtask", response_class=JSONResponse, response_model=TasksModule.Output_Subtask)
async def post_create_subtask(createRequest: RouterRequest_CreateSubtask, req: Request):
    print(createRequest.__dict__)
    newSubtask = TasksModule.Create.subtask(
        TasksModule.Subtask_CreateRequest(**createRequest.__dict__)
    )
    card = TasksModule.RawSelect.oneCard(TasksModule.Card.id == newSubtask.card_id)
    column = TasksModule.RawSelect.oneColumn(TasksModule.Column.id == card.column_id)
    await websocket_broadcast_update(column.board_id)
    return TasksModule.Convert.subtask(newSubtask)

###
###   Endpoints :: Select by ID
###

@router.get("/getBoardById/{id}", response_class=JSONResponse, response_model=TasksModule.Output_Board)
async def get_board_by_id(id: int):
    return TasksModule.Select.oneBoard(TasksModule.Board.id == id)

@router.get("/getColumnById/{id}", response_class=JSONResponse, response_model=TasksModule.Output_Column)
async def get_card_by_id(id: int):
    return TasksModule.Select.oneColumn(TasksModule.Column.id == id)

@router.get("/getCardById/{id}", response_class=JSONResponse, response_model=TasksModule.Output_Card)
async def get_card_by_id(id: int):
    return TasksModule.Select.oneCard(TasksModule.Card.id == id)

@router.get("/getSubtaskById/{id}", response_class=JSONResponse, response_model=TasksModule.Output_Subtask)
async def get_card_by_id(id: int):
    return TasksModule.Select.oneSubtask(TasksModule.Subtask.id == id)

@router.get("/getMyBoards", response_class=JSONResponse, response_model=list[TasksModule.Output_Board])
async def get_my_boards(req: Request):
    return TasksModule.Select.boardsOfUser(req.state.current_user.id)

@router.get("/getBoardsOfGroup/{group_id}", response_class=JSONResponse, response_model=list[TasksModule.Output_Board])
async def get_boards_of_group(group_id: int):
    return TasksModule.Select.boardsOfGroup(group_id)

###
###   Endpoints :: Update
###

@router.post("/updateBoard")
async def post_update_board(updateRequest: RouterRequest_UpdateBoard):
    try:
        result = TasksModule.Update.board(
            TasksModule.Board_UpdateRequest(**updateRequest.__dict__)
        )
        await websocket_broadcast_update(result.id)
        return result
    except:
        return

@router.post("/updateColumn")
async def post_update_column(updateRequest: RouterRequest_UpdateColumn):
    try:
        result = TasksModule.Update.column(
            TasksModule.Column_UpdateRequest(**updateRequest.__dict__)
        )
        await websocket_broadcast_update(result.board_id)
        return result
    except:
        raise HTTPException(status_code=400)

@router.post("/updateMultipleColumns")
async def post_update_column(updateRequestList: list[RouterRequest_UpdateColumn]):
    resultList = []
    boardList = []
    for i in updateRequestList:
        result = TasksModule.Update.column(
            TasksModule.Column_UpdateRequest(**i.__dict__)
        )
        resultList.append(result)
        boardList.append(result.board_id)
    for i in boardList:
        await websocket_broadcast_update(i)
    return resultList

@router.post("/updateCard")
async def post_update_card(updateRequest: RouterRequest_UpdateCard):
    try:
        result = TasksModule.Update.card(
            TasksModule.Card_UpdateRequest(**updateRequest.__dict__)
        )
        column = TasksModule.RawSelect.oneColumn(TasksModule.Column.id == result.column_id)
        await websocket_broadcast_update(column.board_id)
        return result
    except:
        return

@router.post("/updateMultipleCards")
async def post_update_multiple_cards(updateRequestList: list[RouterRequest_UpdateCard]):
    resultList = []
    boardList = []
    for i in updateRequestList:
        result = TasksModule.Update.card(
            TasksModule.Card_UpdateRequest(**i.__dict__)
        )
        resultList.append(result)
        column = TasksModule.RawSelect.oneColumn(TasksModule.Column.id == result.column_id)
        boardList.append(column.board_id)
    for i in boardList:
        await websocket_broadcast_update(i)
    return resultList

@router.post("/updateSubtask")
async def post_update_subtask(updateRequest: RouterRequest_UpdateSubtask):
    try:
        result = TasksModule.Update.subtask(
            TasksModule.Subtask_UpdateRequest(**updateRequest.__dict__)
        )
        card = TasksModule.RawSelect.oneCard(TasksModule.Card.id == result.card_id)
        column = TasksModule.RawSelect.oneColumn(TasksModule.Column.id == card.column_id)
        await websocket_broadcast_update(column.board_id)
        return result
    except:
        return

@router.post("/updateBoardGroup")
async def post_update_board_group(updateRequest: RouterRequest_UpdateBoardGroup):
    try:
        result = TasksModule.Update.boardGroup(
            TasksModule.BoardGroup_UpdateRequest(**updateRequest.__dict__)
        )
        return result
    except:
        return

@router.post("/updateBoardUser")
async def post_update_board_user(updateRequest: RouterRequest_UpdateBoardUser):
    try:
        result = TasksModule.Update.boardUser(
            TasksModule.BoardUser_UpdateRequest(**updateRequest.__dict__)
        )
        return result
    except:
        return

@router.post("/updateCardUser")
async def post_update_card_user(updateRequest: RouterRequest_UpdateCardUser):
    try:
        return TasksModule.Update.cardUser(
            TasksModule.CardUser_UpdateRequest(**updateRequest.__dict__)
        )
    except:
        return

###
###   Endpoints :: Delete
###

###
###   Routers
###

class Connection:
    def __init__(self):
        self.socket = 0
        self.board_id = 0
        self.socket_id = 0

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[Connection] = []
    def getMaxSocketID(self):
        maxid = 0
        for i in self.active_connections:
            if int(i.socket_id) > maxid:
                maxid = int(i.socket_id)
        return maxid
    def getConnectionWithSocket(self, websocket):
        for i in self.active_connections:
            if i.socket == websocket:
                return i
        return -1
    def getConnectionsWithBoardId(self, board_id: int):
        result = []
        for i in self.active_connections:
            if i.board_id == board_id:
                result.append(i)
        return result
    async def connect(self, websocket: WebSocket, board_id: int):
        await websocket.accept()
        newConnection = Connection()
        newConnection.socket = websocket
        newConnection.socket_id = self.getMaxSocketID()+1
        newConnection.board_id = board_id
        print(newConnection.board_id)
        self.active_connections.append(newConnection)
        print("New connection!")
        print(*self.active_connections)
        return newConnection
    def disconnect(self, conn: Connection):
        self.active_connections.remove(conn)
        print(*self.active_connections)
    async def send_personal_message(self, message: str, connection: Connection):
        print(*self.active_connections)
        print("SENDING PERSONAL")
        await connection.socket.send_text(message)

ws_manager = ConnectionManager()

@router_ws.websocket("/ws/{board_id}")
async def websocket_endpoint(websocket: WebSocket, board_id: int):
    newconn = await ws_manager.connect(websocket, board_id)
    while True:
        try:
            data = await websocket.receive_text()
            conn = ws_manager.getConnectionWithSocket(websocket)
        except WebSocketDisconnect:
            conn = ws_manager.getConnectionWithSocket(websocket)
            ws_manager.disconnect(conn)
            break

async def websocket_broadcast_update(board_id: int):
    print("SENDING UPDATE MESSAGE TO", board_id)
    result = ws_manager.getConnectionsWithBoardId(board_id)
    for i in result:
        await ws_manager.send_personal_message("update", i)