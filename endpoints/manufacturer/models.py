from pydantic import BaseModel
from typing import Union


class Manufacturer(BaseModel):
    name: str
    address: Union[str, None] = None
    author_id: int
