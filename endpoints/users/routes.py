from app_logger import logger
from config import (DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, JWT_EXPIRE_MINUTES, LDAP_SERVER_NAME, LDAP_BIND_USER_NAME,
                    LDAP_BIND_USER_PASSWORD)
from .models import User, Token
from .utils import create_access_token, authenticate_user, get_current_user, ldap_register
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
    access_token = ''
    user = authenticate_user(user.name, user.password, 'LDAP')
    if not user.get('name'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    else:
        try:
            user_data = ldap_register(LDAP_SERVER_NAME,
                                      LDAP_BIND_USER_NAME,
                                      LDAP_BIND_USER_PASSWORD,
                                      user.get('name'))
            if user_data['status'] == 'USER_FOUNDED':
                connection = pymysql.connect(host=DB_HOST,
                                             user=DB_USER,
                                             password=DB_PASSWORD,
                                             database=DB_NAME,
                                             cursorclass=pymysql.cursors.DictCursor)
                with connection:
                    with connection.cursor() as cursor:
                        sql = """SELECT * FROM `users` WHERE `login`='{0}'""".format(user_data['login'])
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        if len(result) == 0:
                            sql = """INSERT INTO `users` 
                                                 (`fio`,
                                                  `login`,
                                                  `role`,
                                                  `email`,
                                                  `auth_source`,
                                                  `active`) 
                                     VALUES (%s,%s,%s,%s,%s,%s)"""
                            cursor.execute(sql, (user_data['full_name'],
                                                 user_data['login'],
                                                 3,
                                                 user_data['mail'],
                                                 1,
                                                 1))
                    connection.commit()
                access_token_expires = timedelta(minutes=JWT_EXPIRE_MINUTES)
                access_token = create_access_token(data={'sub': user.get('name')}, expires_delta=access_token_expires)
                return {'access_token': access_token, 'token_type': 'bearer'}
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Incorrect username or password',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
        except Exception as err:
            logger.error(f'Error: {str(err)}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')



@router.get('/check')
async def login(current_user: User = Depends(get_current_user)):
    return current_user
