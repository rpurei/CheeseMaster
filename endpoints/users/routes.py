from app_logger import logger
from config import (DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, JWT_EXPIRE_MINUTES, LDAP_SERVER_NAME, LDAP_BIND_USER_NAME,
                    LDAP_BIND_USER_PASSWORD)
from .models import User, UserInfo, Token
from .utils import create_access_token, authenticate_user, get_current_user, ldap_register
from fastapi import APIRouter, status, HTTPException, Depends, Security
from fastapi.responses import JSONResponse
import pymysql.cursors
from datetime import datetime, timedelta
from jose import JWTError, jwt
import traceback


router = APIRouter(
    prefix='/users',
    tags=['User'],
    responses={404: {'detail': 'Not found'}},
)


@router.post('/login', response_model=Token)
async def login(user: User):
    access_token = ''
    scopes = []
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
                        result = cursor.fetchone()
                        if result is None:
                            sql = """INSERT INTO `users` 
                                                 (`fio`,
                                                  `login`,
                                                  `role_id`,
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
                            scopes = ['user:create',
                                      'user:read',
                                      'user:update',
                                      'user:delete']
                        else:
                            result = dict(result)
                            user_role = result.get('role')
                            if user_role == 1:
                                scopes = ['admin']
                            elif user_role == 2:
                                scopes = ['cheesemaster:create',
                                          'cheesemaster:read',
                                          'cheesemaster:update',
                                          'cheesemaster:delete']
                            elif user_role == 3:
                                scopes = ['user:create',
                                          'user:read',
                                          'user:update',
                                          'user:delete']

                    connection.commit()
                access_token_expires = timedelta(minutes=JWT_EXPIRE_MINUTES)
                access_token = create_access_token(data={'sub': user.get('name'),
                                                         'scopes': scopes}, expires_delta=access_token_expires)
                return {'access_token': access_token, 'token_type': 'bearer'}
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Incorrect username or password',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
        except Exception as err:
            lf = '\n'
            logger.error(f'{traceback.format_exc().replace(lf, "")} : {str(err)}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f'{traceback.format_exc()} : {str(err)}')


@router.get('/info', response_model=UserInfo)
async def info(current_user=Security(get_current_user, scopes=['admin', 'user:read', 'cheesemaster:read'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM `users` WHERE `login`='{0}'""".format(current_user)
                cursor.execute(sql)
                result = cursor.fetchone()
                result = dict(result)
                if result:
                    return {
                        'id': result.get('id'),
                        'login': result.get('login'),
                        'role_id': result.get('role_id'),
                        'fio': result.get('fio'),
                        'email': result.get('email'),
                        'phone': result.get('phone'),
                        'active': result.get('active')
                    }
                else:
                    return JSONResponse(status_code=404,
                                        content={'detail': f'User with login: {current_user} not found.'}, )
    except Exception as err:
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")} : {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'{traceback.format_exc()} : {str(err)}')


@router.get('/orders')
async def info(current_user=Security(get_current_user, scopes=['admin', 'user:read', 'cheesemaster:read'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM `users` WHERE `login`='{0}'""".format(current_user)
                cursor.execute(sql)
                result = cursor.fetchone()
                result = dict(result)
                user_id = result.get('id')
                sql = """SELECT * FROM `orders` WHERE `user_id`='{0}'""".format(user_id)
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
    except Exception as err:
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")} : {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'{traceback.format_exc()} : {str(err)}')


@router.get('/check')
async def login(current_user: User = Depends(get_current_user)):
    return current_user
