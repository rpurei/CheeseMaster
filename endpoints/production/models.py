import datetime
from pydantic import BaseModel
from typing import Union


class ProductionIn(BaseModel):
    date: datetime.date
    product_id: int
    manufacturer_id: int
    warehouse_id: int
    amount: float
    item_measure: str
    comment: Union[str, None] = None
    author_id: int


class ProductionOut(BaseModel):
    id: int
    date: datetime.date
    product_id: int
    manufacturer_id: int
    warehouse_id: int
    amount: float
    item_measure: str
    comment: Union[str, None] = None
    author_id: int
    created: datetime.datetime
    updated: datetime.datetime = None
