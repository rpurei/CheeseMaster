import datetime
from pydantic import BaseModel


class PriceIn(BaseModel):
    product_id: int
    item_measure: str
    item_price: float
    author_id: int


class PriceOut(BaseModel):
    id: int
    product_id: int
    item_measure: str
    item_price: float
    author_id: int
    created: datetime.datetime
    updated: datetime.datetime = None
