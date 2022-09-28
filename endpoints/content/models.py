from ..product.models import ProductOut
from ..manufacturer.models import ManufacturerOut
from ..storage.models import StorageOut
from ..price.models import PriceOut
import datetime
from pydantic import BaseModel
from typing import Union


class ContentIn(BaseModel):
    date: datetime.date
    order_id: int
    product_id: int
    manufacturer_id: int
    storage_id: int = 0
    amount: float
    price_id: int
    status: Union[str, None] = None
    comment: Union[str, None] = None
    author_id: int


class ContentUpdate(BaseModel):
    date: datetime.date
    order_id: int
    product_id: int
    manufacturer_id: int
    storage_id: int
    amount: float
    price_id: int
    status: Union[str, None] = None
    comment: Union[str, None] = None
    author_id: int
    operation: int


class ContentOut(BaseModel):
    id: int
    date: datetime.date
    order_id: int
    product_id: int
    manufacturer_id: int
    storage_id: int
    amount: float
    price_id: int
    status: Union[str, None] = None
    comment: Union[str, None] = None
    author_id: int
    created: datetime.datetime
    updated: datetime.datetime = None


class ContentExtendedOut(BaseModel):
    id: int
    date: datetime.date
    order_id: int
    product: ProductOut
    manufacturer: ManufacturerOut
    storage: StorageOut
    amount: float
    price: PriceOut
    status: Union[str, None] = None
    comment: Union[str, None] = None
    author_id: int
    created: datetime.datetime
    updated: datetime.datetime = None
