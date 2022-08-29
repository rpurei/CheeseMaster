import datetime
from pydantic import BaseModel


class WarehouseIn(BaseModel):
    product_id: int
    amount: float
    item_measure: str
    reserve: float
    active: bool
    author_id: int


class WarehouseOut(BaseModel):
    id: int
    product_id: int
    amount: float
    item_measure: str
    reserve: float
    active: bool
    author_id: int
    created: datetime.datetime
    updated: datetime.datetime = None
