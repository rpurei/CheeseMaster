import datetime
from pydantic import BaseModel
from typing import Union


class Content(BaseModel):
    date: datetime.date
    order_id: int
    product_id: int
    manufacturer_id: int
    warehouse_id: int
    amount: float
    price_id: int
    status: Union[str, None] = None
    comment: Union[str, None] = None
    author_id: int
