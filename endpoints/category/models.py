from pydantic import BaseModel
from typing import Union


class Category(BaseModel):
    name: str
    active: bool = 0
    comment: Union[str, None] = None
    author_id: int

