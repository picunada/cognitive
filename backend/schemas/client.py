from enum import Enum

from pydantic import BaseModel


class Action(Enum):
    activate_id_session = 'activate_id_session'


class CountChange(BaseModel):
    count: int


class Message(BaseModel):
    action: Action
    message: str

