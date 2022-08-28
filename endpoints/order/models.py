import datetime
from pydantic import BaseModel
from typing import Union


class Order(BaseModel):
    date: datetime.date
    delivery_date: datetime.date
    payment_type: int
    status: Union[str, None] = None
    comment: Union[str, None] = None
    author_id: int
