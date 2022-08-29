import datetime
from pydantic import BaseModel
from typing import Union


class PickpointIn(BaseModel):
    name: str
    address: str
    workhours: str
    phone: str
    link_yandex: str
    link_point: str
    map_frame: str
    active: bool = 0
    comment: Union[str, None] = None
    author_id: int


class PickpointOut(BaseModel):
    id: int
    name: str
    address: str
    workhours: str
    phone: str
    link_yandex: str
    link_point: str
    map_frame: str
    active: bool = 0
    comment: Union[str, None] = None
    author_id: int
    created: datetime.datetime
    updated: datetime.datetime = None
