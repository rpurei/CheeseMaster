from pydantic import BaseModel
from typing import Union


class Product(BaseModel):
    name: str
    active: bool
    category_id: int
    comment: Union[str, None] = None
    description: Union[str, None] = None
    author_id: int
    image: str
    ext: str
