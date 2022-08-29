from app_logger import logger
from config import (LDAP_BASE_DN, LDAP_SERVER_NAME, LDAP_BIND_USER_NAME, LDAP_BIND_USER_PASSWORD,
                    JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES)
from .models import TokenData
import ldap
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def ldap_register(address, bind_username, bind_password, user_login):
    conn = ldap.initialize('ldap://' + address)
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    basedn = LDAP_BASE_DN
    searchFilter = f'(&(objectCategory=person)(objectClass=user)(sAMAccountName={user_login}))'
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
    to_encode = data.copy()
    to_encode.update({'exp': datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def check_access_token(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    ct = datetime.now()
    if ct.timestamp() < payload.get('exp', 0):
        return 'TOKEN_VALID'
    else:
        return 'TOKEN_EXPIRED'


async def get_current_user(token: str = Depends(oauth2_scheme)):
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
    if check_access_token(token) == 'TOKEN_EXPIRED':
        raise token_expired_exception
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get('sub')
        if username == '':
            raise credentials_exception
        token_data = TokenData(name=username)
    except JWTError:
        logger.error(credentials_exception)
        raise credentials_exception
    user = token_data.name
    if user == '':
        logger.error(credentials_exception)
        raise credentials_exception
    return user


# if __name__ == '__main__':
#     print(ldap_register(LDAP_SERVER_NAME, LDAP_BIND_USER_NAME, LDAP_BIND_USER_PASSWORD, 'purey.rp'))
#     print(ldap_auth(LDAP_SERVER_NAME, '', ''))