from pydantic import BaseModel


class Warehouse(BaseModel):
    product_id: int
    amount: float
    reserve: float
    author_id: int
