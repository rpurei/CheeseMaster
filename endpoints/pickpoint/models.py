from pydantic import BaseModel
from typing import Union


class Pickpoint(BaseModel):
    address: str
    workhours: str
    phone: str
    link_yandex: str
    link_point: str
    map_frame: str
    active: bool = 0
    comment: Union[str, None] = None
    author_id: int
