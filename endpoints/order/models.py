from ..content.models import ContentOut, ContentExtendedOut
import datetime
from pydantic import BaseModel
from typing import Union, List


class OrderIn(BaseModel):
    user_id: int
    date: datetime.datetime
    delivery_date: datetime.date
    payment_type: int
    status: Union[str, None] = None
    pickpoint_id: int
    comment: Union[str, None] = None
    author_id: int


class OrderOut(BaseModel):
    id: int
    user_id: int
    date: datetime.datetime
    delivery_date: datetime.date
    payment_type: int
    status: Union[str, None] = None
    pickpoint_id: int
    comment: Union[str, None] = None
    author_id: int
    created: datetime.datetime
    updated: datetime.datetime = None


class OrderContentOut(BaseModel):
    id: int
    user_id: int
    date: datetime.datetime
    delivery_date: datetime.date
    payment_type: int
    status: Union[str, None] = None
    pickpoint_id: int
    comment: Union[str, None] = None
    author_id: int
    created: datetime.datetime
    updated: datetime.datetime = None
    content: List[ContentExtendedOut]
