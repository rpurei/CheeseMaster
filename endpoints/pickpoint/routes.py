from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from .models import PickpointIn, PickpointOut
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
import pymysql.cursors


router = APIRouter(
    prefix='/pickpoints',
    tags=['Pickpoint'],
    responses={404: {'detail': 'Not found'}},
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_pickpoint(pickpoint: PickpointIn):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """INSERT INTO `pickpoints` (`NAME`,
                                                       `ADDRESS`,
                                                       `WORKHOURS`,
                                                       `PHONE`,
                                                       `COMMENT`,
                                                       `LINK_YANDEX`,
                                                       `LINK_POINT`,
                                                       `MAP_FRAME`,
                                                       `ACTIVE`,
                                                       `AUTHOR_ID`) 
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
async def update_pickpoint(pickpoint: PickpointIn, pickpoint_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = "SELECT `ID` FROM `pickpoints` WHERE `ID`={0}".format(pickpoint_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = """UPDATE `pickpoints` 
                                 SET `NAME`='{0}',
                                     `ADDRESS`='{1}',
                                     `WORKHOURS`='{2}',
                                     `PHONE`='{3}',
                                     `COMMENT`='{4}',
                                     `LINK_YANDEX`='{5}',
                                     `LINK_POINT`='{6}',
                                     `MAP_FRAME`='{7}',
                                     `ACTIVE`='{8}',
                                     `AUTHOR_ID`='{9}' 
                                 WHERE `ID`={10}""".format(pickpoint.name,
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
                                            content={"detail": f'Pickpoint with ID: {pickpoint_id} not found.'}, )
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'Pickpoint ID {pickpoint_id} updated'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.delete('/{pickpoint_id}', status_code=status.HTTP_200_OK)
async def delete_pickpoint(pickpoint_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT `ID` FROM `pickpoints` WHERE `ID`={0}'.format(pickpoint_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = 'DELETE FROM `pickpoints` WHERE `ID`={0}'.format(pickpoint_id)
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
async def get_pickpoints():
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
async def get_pickpoint(pickpoint_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT * FROM `pickpoints` WHERE `ID`={0}'.format(pickpoint_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    result = dict(result)
                    if len(result) > 0:
                        return {'id': result.get('ID'),
                                'name': result.get('NAME'),
                                'address': result.get('ADDRESS'),
                                'workhours': result.get('WORKHOURS'),
                                'phone': result.get('PHONE'),
                                'link_yandex': result.get('LINK_YANDEX'),
                                'link_point': result.get('LINK_POINT'),
                                'map_frame': result.get('MAP_FRAME'),
                                'active': result.get('ACTIVE'),
                                'comment': result.get('COMMENT'),
                                'author_id': result.get('AUTHOR_ID'),
                                'created': result.get('CREATED'),
                                'updated': result.get('UPDATED')
                                }
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Pickpoint with ID: {pickpoint_id} not found.'},)
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
