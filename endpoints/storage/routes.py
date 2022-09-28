from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from .models import StorageIn, StorageOut
from ..users.utils import get_current_user
from fastapi import APIRouter, status, HTTPException, Security
from fastapi.responses import JSONResponse
import pymysql.cursors


router = APIRouter(
    prefix='/storages',
    tags=['Storage'],
    responses={404: {'detail': 'Not found'}},
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_storage(storage: StorageIn, current_user=Security(get_current_user, scopes=['admin'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """INSERT INTO `storages` (`name`,
                                                     `address`,
                                                     `active`,
                                                     `author_id`) 
                             VALUES (%s,%s,%s,%s)"""
                    cursor.execute(sql, (storage.name,
                                         storage.address,
                                         storage.active,
                                         storage.author_id
                                         ))
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': 'Storage added'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.patch('/{storage_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_storage(storage: StorageIn, storage_id: int, 
                         current_user=Security(get_current_user, scopes=['admin'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = "SELECT `id` FROM `storages` WHERE `id`={0}".format(storage_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        sql = """UPDATE `storages` 
                                 SET `name`='{0}',
                                     `address`='{1}',
                                     `active`='{2}',
                                     `author_id`='{3}' 
                                 WHERE `id`='{4}'""".format(storage.name,
                                                            storage.address,
                                                            storage.active,
                                                            storage.author_id,
                                                            storage_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Storage with ID: {storage_id} not found.'}, )
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'Storage ID {storage_id} updated'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.delete('/{storage_id}', status_code=status.HTTP_200_OK)
async def delete_storage(storage_id: int, current_user=Security(get_current_user, scopes=['superadmin'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT `id` FROM `storages` WHERE `id`='{0}'""".format(storage_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        sql = """DELETE FROM `storages` WHERE `id`='{0}'""".format(storage_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Storage with ID: {storage_id} not found.'},)
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'Storage ID: {storage_id} deleted'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_storages(current_user=Security(get_current_user, scopes=['storage:read'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT * FROM `storages`'
                    cursor.execute(sql)
                    result = cursor.fetchall()
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            return result
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


def get_storage_by_id(storage_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT * FROM `storages` WHERE `id`='{0}'""".format(storage_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    result = dict(result)
                    if result:
                        return {'id': result.get('id'),
                                'name': result.get('name'),
                                'address': result.get('address'),
                                'active': result.get('active'),
                                'comment': result.get('comment'),
                                'author_id': result.get('author_id'),
                                'created': result.get('created'),
                                'updated': result.get('updated')
                                }
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Storage with ID: {storage_id} not found.'},)
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/{storage_id}', status_code=status.HTTP_200_OK, response_model=StorageOut)
async def get_storage(storage_id: int, current_user=Security(get_current_user, scopes=['storage:read'])):
    get_storage_by_id(storage_id)
