import datetime
from pydantic import BaseModel
from typing import Union


class ContentIn(BaseModel):
    date: datetime.date
    order_id: int
    product_id: int
    manufacturer_id: int
    storage_id: int = 0
    amount: float
    price_id: int
    status: Union[str, None] = None
    comment: Union[str, None] = None
    author_id: int


class ContentOut(BaseModel):
    id: int
    date: datetime.date
    order_id: int
    product_id: int
    manufacturer_id: int
    storage_id: int = 0
    amount: float
    price_id: int
    status: Union[str, None] = None
    comment: Union[str, None] = None
    author_id: int
    created: datetime.datetime
    updated: datetime.datetime = None
