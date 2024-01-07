
from pydantic import BaseModel, Field
from typing import Optional
from fastapi import UploadFile as FastAPI_UploadFile

#############################################################################################################################

###
###   Requests
###

#############################################################################################################################

###
###   Files :: Create
###

class File_CreateRequest(BaseModel):
    title: str
    owner_id: int
    parent_folder_id: int
    users_can_view: Optional[list[int]] = []
    users_can_edit: Optional[list[int]] = []
    groups_can_view: Optional[list[int]] = []
    groups_can_edit: Optional[list[int]] = []
    unrestricted_view_access: Optional[bool] = False
    unrestricted_edit_access: Optional[bool] = False
    inheritView: Optional[bool] = False
    inheritEdit: Optional[bool] = False
    file: FastAPI_UploadFile
    """
    class Config:
        validate_assignment = True
    @validator('users_can_view')
    def set_users_can_view(cls, users_can_view): return users_can_view or []
    @validator('users_can_edit')
    def set_users_can_edit(cls, users_can_edit): return users_can_edit or []
    @validator('groups_can_view')
    def set_groups_can_view(cls, groups_can_view): return groups_can_view or []
    @validator('groups_can_edit')
    def set_groups_can_edit(cls, groups_can_edit): return groups_can_edit or []
    @validator('unrestricted_view_access')
    def set_unrestricted_view_access(cls, unrestricted_view_access): return unrestricted_view_access or False
    @validator('unrestricted_edit_access')
    def set_unrestricted_edit_access(cls, unrestricted_edit_access): return unrestricted_edit_access or False
    @validator('inheritView')
    def set_inheritView(cls, inheritView): return inheritView or False
    @validator('inheritEdit')
    def set_inheritEdit(cls, inheritEdit): return inheritEdit or False
    """

class File_CreateRequestForExisting(BaseModel):
    title: str
    owner_id: int
    parent_folder_id: int
    users_can_view: list[int] = Field(default=[])
    users_can_edit: list[int] = Field(default=[])
    groups_can_view: list[int] = Field(default=[])
    groups_can_edit: list[int] = Field(default=[])
    unrestricted_view_access: bool = Field(default=False)
    unrestricted_edit_access: bool = Field(default=False)
    filepath: str

class Folder_CreateRequest(BaseModel):
    title: str
    max_size: Optional[int]
    owner_id: int
    parent_folder_id: Optional[int]
    users_can_view: list[int] = Field(default=[])
    users_can_edit: list[int] = Field(default=[])
    groups_can_view: list[int] = Field(default=[])
    groups_can_edit: list[int] = Field(default=[])
    unrestricted_view_access: bool = Field(default=False)
    unrestricted_edit_access: bool = Field(default=False)
    inheritView: bool = Field(default=False)
    inheritEdit: bool = Field(default=False)

class FolderUser_CreateRequest(BaseModel):
    folder_id: int
    user_id: int
    can_view: bool
    can_edit: bool

class FileUser_CreateRequest(BaseModel):
    file_id: int
    user_id: int
    can_view: bool
    can_edit: bool

class FolderGroup_CreateRequest(BaseModel):
    folder_id: int
    group_id: int
    can_view: bool
    can_edit: bool
    
class FileGroup_CreateRequest(BaseModel):
    file_id: int
    group_id: int
    can_view: bool
    can_edit: bool

###
###   Files :: Update
###

class File_UpdateRequest(BaseModel):
    id: int
    title: Optional[str]
    owner_id: Optional[int]
    parent_folder_id: Optional[int]
    users_can_view: Optional[list[int]]
    users_can_edit: Optional[list[int]]
    groups_can_view: Optional[list[int]]
    groups_can_edit: Optional[list[int]]
    unrestricted_view_access: Optional[bool]
    unrestricted_edit_access: Optional[bool]
    file: FastAPI_UploadFile

class Folder_UpdateRequest(BaseModel):
    id: int
    title: Optional[str]
    max_size: Optional[int]
    owner_id: Optional[int]
    parent_folder_id: Optional[int]
    users_can_view: Optional[list[int]]
    users_can_edit: Optional[list[int]]
    groups_can_view: Optional[list[int]]
    groups_can_edit: Optional[list[int]]
    unrestricted_view_access: Optional[bool]
    unrestricted_edit_access: Optional[bool]

class FolderUser_UpdateRequest(BaseModel):
    folder_id: int
    user_id: int
    can_view: Optional[bool]
    can_edit: Optional[bool]

class FileUser_UpdateRequest(BaseModel):
    file_id: int
    user_id: int
    can_view: Optional[bool]
    can_edit: Optional[bool]

class FolderGroup_UpdateRequest(BaseModel):
    folder_id: int
    group_id: int
    can_view: Optional[bool]
    can_edit: Optional[bool]

class FileGroup_UpdateRequest(BaseModel):
    file_id: int
    group_id: int
    can_view: Optional[bool]
    can_edit: Optional[bool]

#############################################################################################################################

###
###   Messages
###
    
class Conversation_CreateRequest(BaseModel):
    type: str
    allowed_from1: int
    allowed_from2: Optional[int]

class Message_CreateRequest(BaseModel):
    conversation_id: int
    text: str
    new_media: Optional[list[FastAPI_UploadFile]] = []
    existing_media: Optional[list[int]] = []
    sender_id: int
    shared_message_id: Optional[int]

class Message_UpdateRequest(BaseModel):
    id: int
    text: Optional[str]

#############################################################################################################################
    
###
###   Users: Create
###

class User_CreateRequest(BaseModel):
    handle: str
    visible_name: str
    email: str
    password_hash: str

###
###   Users: Update
###

class User_UpdateRequest(BaseModel):
    id: int
    handle: Optional[str]
    visible_name: Optional[str]
    email: Optional[str]
    password_hash: Optional[str]
    join_date: Optional[int]
    avatar_fileid: Optional[int]
    bio: Optional[str]
    contacts: Optional[list[int]]
    notifications: Optional[list[dict]]
    events: Optional[list[dict]]
    fav_users: Optional[list[int]]
    fav_groups: Optional[list[int]]
    # folder_id: Optional[int]
    is_admin: Optional[bool]

#############################################################################################################################
    
###
###   Groups: Create
###

class Group_CreateRequest(BaseModel):
    title: str = Field()
    owner_id: int

class Channel_CreateRequest(BaseModel):
    title: str = Field()
    group_id: int = Field()
    owner_id: int = Field()
    is_primary: bool = Field()

class GroupUser_CreateRequest(BaseModel):
    user_id: int
    group_id: int

###
###   Groups: Update
###

class Group_UpdateRequest(BaseModel):
    title: Optional[str]
    avatar_fileid: Optional[int]
    color: Optional[str]
    users: Optional[int]

class Channel_UpdateRequest(BaseModel):
    title: Optional[str]
    is_primary: bool

#############################################################################################################################

###
###   Tasks :: Create
###

class Board_CreateRequest(BaseModel):
    title: str
    owner_id: int

class Column_CreateRequest(BaseModel):
    title: str = Field()
    board_id: int = Field()
    position_x: int = Field()

class Card_CreateRequest(BaseModel):
    title: str = Field()
    description: str = Field(nullable=True)
    column_id: int = Field()
    position_y: int = Field()
    color: str = Field()
    owner_id: int = Field()

class Subtask_CreateRequest(BaseModel):
    text: str
    card_id: int
    position: int

class BoardGroup_CreateRequest(BaseModel):
    board_id: int
    group_id: int
    can_view: bool
    can_edit: bool

class BoardUser_CreateRequest(BaseModel):
    board_id: int
    user_id: int
    can_view: bool
    can_edit: bool

class CardUser_CreateRequest(BaseModel):
    card_id: int
    user_id: int
    can_edit: bool

###
###   Tasks :: Update
###

class Board_UpdateRequest(BaseModel):
    id: int
    title: Optional[str]
    owner_id: Optional[int]

class Column_UpdateRequest(BaseModel):
    id: int
    board_id: Optional[int]
    title: Optional[str]
    position_x: Optional[int]

class Card_UpdateRequest(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    column_id: Optional[int]
    position_y: Optional[int]
    color: Optional[str]
    owner_id: Optional[int]
    deadline: Optional[int]
    attached_files: Optional[list[int]]

class Subtask_UpdateRequest(BaseModel):
    id: int
    text: Optional[str]
    card_id: Optional[int]
    position: Optional[int]
    is_done: Optional[bool]

class BoardUser_UpdateRequest(BaseModel):
    board_id: int
    user_id: int
    can_view: Optional[bool]
    can_edit: Optional[bool]

class BoardGroup_UpdateRequest(BaseModel):
    board_id: int
    group_id: int
    can_view: Optional[bool]
    can_edit: Optional[bool]

class CardUser_UpdateRequest(BaseModel):
    card_id: int
    user_id: int
    can_edit: Optional[bool]

#############################################################################################################################