from pydantic import BaseModel
from typing import Union
import datetime


class ManufacturerIn(BaseModel):
    name: str
    address: Union[str, None] = None
    author_id: int


class ManufacturerOut(BaseModel):
    id: int
    name: str
    address: Union[str, None] = None
    author_id: int
    created: datetime.datetime
    updated: datetime.datetime = None
