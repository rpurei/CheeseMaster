from pydantic import BaseModel
from typing import Union


class Pickpoint(BaseModel):
    address: str
    workhours: str
    available: bool = 0
    comment: Union[str, None] = None
    author_id: int
