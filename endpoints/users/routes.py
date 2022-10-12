from app_logger import logger
from config import (DB_HOST, DB_NAME, DB_USER, DB_PASSWORD,
                    JWT_EXPIRE_MINUTES,
                    LDAP_SERVER_NAME, LDAP_BIND_USER_NAME, LDAP_BIND_USER_PASSWORD,
                    MAIL_HOST, MAIL_PORT, MAIL_USER, MAIL_PASS)
from .models import User, UserInfo, Token, UserUpdate, MailMessage
from .utils import create_access_token, authenticate_user, get_current_user, ldap_register
from fastapi import APIRouter, status, HTTPException, Depends, Security
from fastapi.responses import JSONResponse
import pymysql.cursors
from datetime import datetime, timedelta
from jose import JWTError, jwt
import traceback
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


user_scopes = ['user:read',
              'user:update',
              'product:read',
              'category:read',
              'content:read',
              'content:create',
              'content:update',
              'content:delete',
              'manufacturer:read',
              'order:create',
              'order:update',
              'pickpoint:read',
              'price:read',
              'self:read'
              ]

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
                            scopes = user_scopes
                        else:
                            result = dict(result)
                            user_role = result.get('role_id')
                            if user_role == 1:
                                scopes = ['admin',
                                          'user:read',
                                          'user:update',
                                          'user:delete',
                                          'product:read',
                                          'product:create',
                                          'product:update',
                                          'category:read',
                                          'category:update',
                                          'category:create',
                                          'content:read',
                                          'content:create',
                                          'content:update',
                                          'content:delete',
                                          'manufacturer:read',
                                          'order:create',
                                          'order:update',
                                          'order:read',
                                          'pickpoint:read',
                                          'price:read',
                                          'production:read',
                                          'production:update',
                                          'production:create',
                                          'storage:read',
                                          'warehouse:read',
                                          'user:read',
                                          'self:read'
                                          ]
                            elif user_role == 2:
                                scopes = ['user:read',
                                          'product:read',
                                          'product:create',
                                          'product:update',
                                          'category:read',
                                          'category:update'
                                          'category:create',
                                          'content:read',
                                          'content:create',
                                          'content:update',
                                          'content:delete',
                                          'manufacturer:read',
                                          'order:create',
                                          'order:update',
                                          'order:read',
                                          'pickpoint:read',
                                          'price:read',
                                          'production:read',
                                          'production:update',
                                          'production:create',
                                          'storage:read',
                                          'warehouse:read',
                                          'user:read',
                                          'self:read'
                                          ]
                            elif user_role == 3:
                                scopes = user_scopes
                            elif user_role == 4:
                                scopes = ['user:read',
                                          'product:read',
                                          'category:read',
                                          'content:read',
                                          'content:create',
                                          'content:update',
                                          'content:delete',
                                          'manufacturer:read',
                                          'order:update',
                                          'order:read',
                                          'pickpoint:read',
                                          'price:read',
                                          'production:read',
                                          'storage:read',
                                          'warehouse:read',
                                          'user:read',
                                          'self:read'
                                          ]
                            else:
                                raise ValueError('Unknown role')
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
async def get_user_info(current_user=Security(get_current_user, scopes=['self:read'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                # sql = """SELECT * FROM `users` WHERE `login`='{0}'""".format(current_user)
                sql = """SELECT usr.id,
                                usr.guid,
                                usr.login,
                                rls.title,
                                usr.fio,
                                usr.email,
                                usr.phone,
                                usr.auth_source,
                                usr.active,
                                usr.created,
                                usr.created,
                                rls.id as 'role_id'
                         FROM `users` usr LEFT JOIN `user_roles` rls ON usr.role_id = rls.id
                         WHERE usr.login = '{0}'""".format(current_user)
                cursor.execute(sql)
                result = cursor.fetchone()
                result = dict(result)
                if result:
                    return {
                        'id': result.get('id'),
                        'login': result.get('login'),
                        'role': result.get('title'),
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
async def get_user_orders(limit: int = 100000, offset: int = 0,
                          current_user=Security(get_current_user, scopes=['self:read'])):
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
                    user_id = result.get('id')
                    sql = f"""SELECT * FROM `orders` WHERE `user_id`='{user_id}' LIMIT {limit} OFFSET {offset}"""
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
                else:
                    return JSONResponse(status_code=404,
                                        content={'detail': f'User with login: {current_user} not found.'}, )
    except Exception as err:
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")} : {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'{traceback.format_exc()} : {str(err)}')


@router.get('/')
async def get_users(limit: int = 100000, offset: int = 0,
                    current_user=Security(get_current_user, scopes=['user:read'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = f"""SELECT u.id,
                                 u.login,
                                 ur.title,
                                 u.role_id,
                                 u.fio,
                                 u.email,
                                 u.phone,
                                 u.active,
                                 u.auth_source,
                                 u.created,
                                 u.updated
                         FROM `users` u
                         LEFT JOIN user_roles ur on u.role_id = ur.id
                         LIMIT {limit} OFFSET {offset}"""
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
    except Exception as err:
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")} : {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'{traceback.format_exc()} : {str(err)}')


@router.patch('/{user_id}')
async def user_edit(user_id: int, user: UserUpdate, current_user=Security(get_current_user, scopes=['user:read'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM `users` WHERE `id`='{0}'""".format(user_id)
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    sql = """UPDATE `users` SET `role_id`='{0}',
                                                `phone`='{1}',
                                                `active`='{2}' 
                             WHERE `id`='{3}'""".format(user.role_id,
                                                      user.phone,
                                                      user.active,
                                                      user_id)
                    cursor.execute(sql)
                else:
                    return JSONResponse(status_code=404,
                                        content={'detail': f'User with login: {current_user} not found.'}, )
            connection.commit()
    except Exception as err:
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")} : {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'{traceback.format_exc()} : {str(err)}')


@router.post('/sendmail')
async def sendmail(mail_message: MailMessage, current_user=Security(get_current_user, scopes=['user:read'])):
    context = ssl._create_unverified_context()
    server = None
    message = MIMEMultipart('alternative')
    message['Subject'] = mail_message.subject
    message['From'] = MAIL_USER
    message['To'] = mail_message.address
    part = MIMEText(mail_message.body, "plain")
    message.attach(part)
    try:
        server = smtplib.SMTP(MAIL_HOST, MAIL_PORT)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(MAIL_USER, MAIL_PASS)
        server.sendmail(MAIL_USER, mail_message.address, message.as_string().encode('utf-8'))
    except Exception as err:
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")} : {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'{traceback.format_exc()} : {str(err)}')
    finally:
        server.quit()
