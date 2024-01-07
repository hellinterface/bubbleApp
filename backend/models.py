from pydantic import BaseModel, Field
from typing import Optional

###
###   Models :: Users
###

class Output_User(BaseModel):
    id: Optional[int]
    handle: str
    visible_name: str
    email: str
    avatar_fileid: Optional[int]
    bio: str
    contacts: list[int]
    notifications: list[dict]
    events: list[dict]
    folder_id: int
    sent_media_folder_id: int
    fav_users: list[int]
    fav_groups: list[int]

class PublicOutput_User(BaseModel):
    id: Optional[int]
    handle: str
    visible_name: str
    email: str
    avatar_fileid: Optional[int]
    bio: str

###
###   Models :: Groups
###

class Output_Channel(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int
    title: str
    is_primary: bool
    users: list[PublicOutput_User] = Field(default=[])

class Output_Group(BaseModel):
    id: Optional[int] = Field(default=None)
    title: str
    avatar_fileid: Optional[int]
    folder_id: str
    color: str
    owner: PublicOutput_User
    users: list[PublicOutput_User] = Field(default=[])
    channels: list[Output_Channel] = Field(default=[])

###
###   Models :: Files
###

class Output_FilesUserEntry(BaseModel):
    user_information: PublicOutput_User
    can_view: bool
    can_edit: bool
    
class Output_FilesGroupEntry(BaseModel):
    group_information: Output_Group
    can_view: bool
    can_edit: bool

class Output_File(BaseModel):
    id: int
    title: str
    date_added: int
    date_modified: int
    owner: PublicOutput_User
    user_modified: PublicOutput_User
    share_link: str
    size: int
    parent_folder_id: Optional[int]
    users: list[Output_FilesUserEntry]
    groups: list[Output_FilesGroupEntry]
    unrestricted_view_access: bool
    unrestricted_edit_access: bool

class Output_Folder(BaseModel):
    id: int
    title: str
    owner: PublicOutput_User
    max_size: Optional[int]
    share_link: str
    parent_folder_id: Optional[int]
    users: list[Output_FilesUserEntry]
    groups: list[Output_FilesGroupEntry]
    unrestricted_view_access: bool
    unrestricted_edit_access: bool

class Output_FileInList(BaseModel):
    id: int
    title: str
    date_added: int
    date_modified: int
    owner: PublicOutput_User
    user_modified: PublicOutput_User
    share_link: str
    size: int

class Output_FolderInList(BaseModel):
    id: int
    title: str
    owner: PublicOutput_User
    max_size: Optional[int]
    share_link: str

class Output_FolderContents(BaseModel):
    folders: list[Output_FolderInList]
    files: list[Output_FileInList]

###
###   Models :: Messaging
###

class Output_Message(BaseModel):
    id: int
    text: str
    edited: bool
    sender: PublicOutput_User
    time: int
    media_ids: list[int]
    shared_message: Optional['Output_Message']

class Output_PersonalConversation(BaseModel):
    id: int
    other_user: PublicOutput_User

###
###   Models :: Tasks
###

class Output_TasksUserEntry(BaseModel):
    user_information: PublicOutput_User
    can_view: bool
    can_edit: bool

class Output_TasksGroupEntry(BaseModel):
    group_information: Output_Group
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
    owner: Output_TasksUserEntry
    deadline: Optional[int]
    users: list[Output_TasksUserEntry]
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
    owner: Output_TasksUserEntry
    users: list[Output_TasksUserEntry]
    groups: list[Output_TasksGroupEntry]
    columns: list[Output_Column]
