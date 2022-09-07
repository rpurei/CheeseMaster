import datetime
from pydantic import BaseModel
from typing import Union


class OrderIn(BaseModel):
    date: datetime.date
    delivery_date: datetime.date
    payment_type: int
    status: Union[str, None] = None
    pickpoint_id: int
    comment: Union[str, None] = None
    author_id: int


class OrderOut(BaseModel):
    id: int
    date: datetime.date
    delivery_date: datetime.date
    payment_type: int
    status: Union[str, None] = None
    pickpoint_id: int
    comment: Union[str, None] = None
    author_id: int
    created: datetime.datetime
    updated: datetime.datetime = None
