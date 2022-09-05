import datetime
from pydantic import BaseModel
from typing import Union


class StorageIn(BaseModel):
    name: str
    address: str
    active: int = 0
    comment: Union[str, None] = None
    author_id: int


class StorageOut(BaseModel):
    id: int
    name: str
    address: str
    active: int = 0
    comment: Union[str, None] = None
    author_id: int
    created: datetime.datetime
    updated: datetime.datetime = None
