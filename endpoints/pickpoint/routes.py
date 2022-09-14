from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from .models import PickpointIn, PickpointOut
from ..users.utils import get_current_user
from fastapi import APIRouter, status, HTTPException, Security
from fastapi.responses import JSONResponse
import pymysql.cursors


router = APIRouter(
    prefix='/pickpoints',
    tags=['Pickpoint'],
    responses={404: {'detail': 'Not found'}},
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_pickpoint(pickpoint: PickpointIn, current_user = Security(get_current_user, scopes=['admin'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """INSERT INTO `pickpoints` (`name`,
                                                       `address`,
                                                       `workhours`,
                                                       `phone`,
                                                       `comment`,
                                                       `link_yandex`,
                                                       `link_point`,
                                                       `map_frame`,
                                                       `active`,
                                                       `author_id`) 
                             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(sql, (pickpoint.name,
                                         pickpoint.address,
                                         pickpoint.workhours,
                                         pickpoint.phone,
                                         pickpoint.comment,
                                         pickpoint.link_yandex,
                                         pickpoint.link_point,
                                         pickpoint.map_frame,
                                         pickpoint.active,
                                         pickpoint.author_id
                                         ))
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': 'Pickpoint added'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.patch('/{pickpoint_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_pickpoint(pickpoint: PickpointIn, pickpoint_id: int, current_user = Security(get_current_user,
                                                                                              scopes=['admin'])):

    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = "SELECT `id` FROM `pickpoints` WHERE `id`={0}".format(pickpoint_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        sql = """UPDATE `pickpoints` 
                                 SET `name`='{0}',
                                     `address`='{1}',
                                     `workhours`='{2}',
                                     `phone`='{3}',
                                     `comment`='{4}',
                                     `link_yandex`='{5}',
                                     `link_point`='{6}',
                                     `map_frame`='{7}',
                                     `active`='{8}',
                                     `author_id`='{9}' 
                                 WHERE `id`='{10}'""".format(pickpoint.name,
                                                           pickpoint.address,
                                                           pickpoint.workhours,
                                                           pickpoint.phone,
                                                           pickpoint.comment,
                                                           pickpoint.link_yandex,
                                                           pickpoint.link_point,
                                                           pickpoint.map_frame,
                                                           pickpoint.active,
                                                           pickpoint.author_id,
                                                           pickpoint_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Pickpoint with ID: {pickpoint_id} not found.'}, )
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'Pickpoint ID {pickpoint_id} updated'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.delete('/{pickpoint_id}', status_code=status.HTTP_200_OK)
async def delete_pickpoint(pickpoint_id: int, current_user = Security(get_current_user, scopes=['superadmin'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT `id` FROM `pickpoints` WHERE `id`='{0}'""".format(pickpoint_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        sql = """DELETE FROM `pickpoints` WHERE `id`='{0}'""".format(pickpoint_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Pickpoint with ID: {pickpoint_id} not found.'},)
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'Pickpoint ID: {pickpoint_id} deleted'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_pickpoints(current_user = Security(get_current_user, scopes=['admin',
                                                                           'user:read',
                                                                           'cheesemaster:read'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT * FROM `pickpoints`'
                    cursor.execute(sql)
                    result = cursor.fetchall()
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            return result
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/{pickpoint_id}', status_code=status.HTTP_200_OK, response_model=PickpointOut)
async def get_pickpoint(pickpoint_id: int, current_user = Security(get_current_user, scopes=['admin',
                                                                                             'user:read',
                                                                                             'cheesemaster:read'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT * FROM `pickpoints` WHERE `id`='{0}'""".format(pickpoint_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    result = dict(result)
                    if result:
                        return {'id': result.get('id'),
                                'name': result.get('name'),
                                'address': result.get('address'),
                                'workhours': result.get('workhours'),
                                'phone': result.get('phone'),
                                'link_yandex': result.get('link_yandex'),
                                'link_point': result.get('link_point'),
                                'map_frame': result.get('map_frame'),
                                'active': result.get('active'),
                                'comment': result.get('comment'),
                                'author_id': result.get('author_id'),
                                'created': result.get('created'),
                                'updated': result.get('updated')
                                }
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Pickpoint with ID: {pickpoint_id} not found.'},)
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
