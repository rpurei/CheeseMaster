from pydantic import BaseModel
from typing import Union
import datetime


class CategoryIn(BaseModel):
    name: str
    active: int = 0
    comment: Union[str, None] = None
    author_id: int


class CategoryOut(BaseModel):
    id: int
    name: str
    active: int = 0
    comment: Union[str, None] = None
    author_id: int
    created: datetime.datetime
    updated: datetime.datetime = None
