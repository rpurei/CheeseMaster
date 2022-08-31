import datetime
from pydantic import BaseModel
from typing import Union


class ProductIn(BaseModel):
    name: str
    active: int
    category_id: int
    comment: Union[str, None] = None
    description: Union[str, None] = None
    author_id: int
    image: str
    ext: str


class ProductOut(BaseModel):
    id: int
    name: str
    active: int
    category_id: int
    comment: Union[str, None] = None
    description: Union[str, None] = None
    author_id: int
    image_path: str
    created: datetime.datetime
    updated: datetime.datetime = None
