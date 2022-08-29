from app_logger import logger
from config import (DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_SECRET_KEY,
                    LDAP_SERVER_NAME)
from .models import User, Token
from .utils import create_access_token, authenticate_user, check_access_token
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
import pymysql.cursors
from datetime import datetime, timedelta
from jose import JWTError, jwt


router = APIRouter(
    prefix='/users',
    tags=['User'],
    responses={404: {'detail': 'Not found'}},
)


@router.post('/login', response_model=Token)
async def login(user: User):
    user = authenticate_user(user.name, user.password, 'LDAP')
    if not user.get('name'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    else:
        access_token_expires = timedelta(minutes=JWT_EXPIRE_MINUTES)
        access_token = create_access_token(data={'sub': user.get('name')}, expires_delta=access_token_expires)
        return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/check')
async def login(token: Token):
    check_access_token(token.access_token)
