from pydantic import BaseModel


class Warehouse(BaseModel):
    product_id: int
    amount: float
    item_measure: str
    reserve: float
    active: bool
    author_id: int
