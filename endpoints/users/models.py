import datetime
from pydantic import BaseModel, EmailStr
from typing import Union, List
from enum import Enum


class User(BaseModel):
    name: str
    password: str


class UserInfo(BaseModel):
    id: int
    login: str
    role: str
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


class MailMessage(BaseModel):
    address: EmailStr
    subject: str
    body: str


class RequestRoles(str, Enum):
    admin = 'admin'
    cheesemaster = 'cheesemaster'
