from pydantic import BaseModel


class Price(BaseModel):
    product_id: int
    item_measure: str
    item_price: float
    author_id: int
