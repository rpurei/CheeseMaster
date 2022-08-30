import datetime
from pydantic import BaseModel
from typing import Union, List


class User(BaseModel):
    name: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: Union[str, None] = None
    scopes: List[str] = []
