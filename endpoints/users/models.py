import datetime
from pydantic import BaseModel
from typing import Union, List


class User(BaseModel):
    name: str
    password: str


class UserInfo(BaseModel):
    id: int
    login: str
    role_id: int
    fio: str
    email: str
    phone: Union[str, None] = None
    active: int


class UserUpdate(BaseModel):
    role_id: int
    phone: Union[str, None] = None
    active: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: Union[str, None] = None
    scopes: List[str] = []

