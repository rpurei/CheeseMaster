from pydantic import BaseModel
from typing import Union


class Product(BaseModel):
    name: str
    available: bool
    category_id: int
    comment: Union[str, None] = None
    author_id: int
    image_path: str
