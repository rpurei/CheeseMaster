from app_logger import logger
from config import (LDAP_BASE_DN, LDAP_SERVER_NAME, LDAP_BIND_USER_NAME, LDAP_BIND_USER_PASSWORD,
                    JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES, DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
from .models import TokenData
import ldap
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
import pymysql.cursors

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login',
                                     scopes={'admin': 'Admin access',
                                             'cheesemaster:create': 'Write items',
                                             'cheesemaster:read': 'Read items',
                                             'cheesemaster:update': 'Update items',
                                             'cheesemaster:delete': 'Delete items',
                                             'user:create': 'Write items',
                                             'user:read': 'Read items',
                                             'user:update': 'Update items',
                                             'user:delete': 'Delete items',
                                             })


def ldap_register(address, bind_username, bind_password, user_login):
    conn = ldap.initialize('ldap://' + address)
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    basedn = LDAP_BASE_DN
    searchFilter = f'(&(objectCategory=person)(objectClass=user)(mail={user_login}))'
    searchAttribute = ['mail', 'cn']
    searchScope = ldap.SCOPE_SUBTREE
    register_result = {'status': '', 'login': '', 'mail': '', 'full_name': ''}
    try:
        result = conn.simple_bind_s(bind_username, bind_password)
        try:
            ldap_result_id = conn.search(basedn, searchScope, searchFilter, searchAttribute)
            while 1:
                result_type, result_data = conn.result(ldap_result_id, 0)
                if result_data == []:
                    register_result['status'] = 'USER_NOT_FOUNDED'
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        register_result['full_name'] = result_data[0][1]['cn'][0].decode('utf-8')
                        register_result['login'] = user_login
                        register_result['mail'] = result_data[0][1]['mail'][0].decode('utf-8')
            if len(register_result['login']) > 0:
                register_result['status'] = 'USER_FOUNDED'
        except ldap.LDAPError as e:
            print(e)
    except ldap.INVALID_CREDENTIALS:
        register_result['status'] = 'LDAP_SRV_INVALID_CRED'
    except ldap.SERVER_DOWN:
        register_result['status'] = 'LDAP_SRV_UNREACH'
    except ldap.LDAPError as e:
        register_result['status'] = f'LDAP_OTHER_ERROR: {str(e)}'
    finally:
        conn.unbind_s()
    return register_result


def ldap_auth(address, bind_username, bind_password):
    conn = ldap.initialize('ldap://' + address)
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    register_result = {'status': ''}
    try:
        result = conn.simple_bind_s(bind_username, bind_password)
        register_result['status'] = 'USER_AUTHENTICATED'
        register_result['username'] = bind_username
    except ldap.INVALID_CREDENTIALS:
        register_result['status'] = 'LDAP_SRV_INVALID_CRED'
    except ldap.SERVER_DOWN:
        register_result['status'] = 'LDAP_SRV_UNREACH'
    except ldap.LDAPError as e:
        register_result['status'] = f'LDAP_OTHER_ERROR: {str(e)}'
    finally:
        conn.unbind_s()
    return register_result


def authenticate_user(username: str, password: str, type: str):
    user = {}
    if type == 'LDAP':
        result = ldap_auth(LDAP_SERVER_NAME, username, password)
        if result['status'] == 'USER_AUTHENTICATED' and result.get('username'):
            user['name'] = result.get('username')
    else:
        logger.error('Unknown authentication method')
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    data_encode = data.copy()
    data_encode.update({'exp': datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(data_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def check_access_token(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    ct = datetime.now()
    if ct.timestamp() < payload.get('exp', 0):
        return 'TOKEN_VALID'
    else:
        return 'TOKEN_EXPIRED'


def get_user(username: str):
    user = ''
    connection = pymysql.connect(host=DB_HOST,
                                 user=DB_USER,
                                 password=DB_PASSWORD,
                                 database=DB_NAME,
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            sql = """SELECT * FROM `users` WHERE `login`='{0}'""".format(username)
            cursor.execute(sql)
            result = cursor.fetchone()
            result = dict(result)
            user = result.get('login')
    return user


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    user = ''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    token_expired_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Access token expired',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = 'Bearer'
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': authenticate_value},
    )
    if check_access_token(token) == 'TOKEN_EXPIRED':
        raise token_expired_exception
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get('sub')
        token_scopes = payload.get('scopes', [])
        token_data = TokenData(scopes=token_scopes, name=username)
        if username == '':
            raise credentials_exception
    except JWTError:
        logger.error(credentials_exception)
        raise credentials_exception
    user = get_user(token_data.name)
    if user == '':
        logger.error(credentials_exception)
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not enough permissions',
                headers={'WWW-Authenticate': authenticate_value},
            )
    return user


#if __name__ == '__main__':
    # print(ldap_register(LDAP_SERVER_NAME, LDAP_BIND_USER_NAME, LDAP_BIND_USER_PASSWORD, 'purey.rp@zdmail.ru'))
    # print(ldap_auth(LDAP_SERVER_NAME, '', ''))