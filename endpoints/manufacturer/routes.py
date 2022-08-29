from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from .models import ManufacturerIn, ManufacturerOut
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
import pymysql.cursors


router = APIRouter(
    prefix='/manufacturers',
    tags=['Manufacturer'],
    responses={404: {'detail': 'Not found'}},
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_manufacturer(manufacturer: ManufacturerIn):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'INSERT INTO `manufacturers` (`NAME`,`ADDRESS`,`AUTHOR_ID`) VALUES (%s,%s,%s)'
                    cursor.execute(sql, (manufacturer.name,
                                         manufacturer.address,
                                         manufacturer.author_id
                                         ))
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': 'Manufacturer added'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.patch('/{manufacturer_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_manufacturer(manufacturer: ManufacturerIn, manufacturer_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT `ID` FROM `manufacturers` WHERE `ID`={0}'.format(manufacturer_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = """UPDATE `manufacturers` 
                                 SET `NAME`='{0}',
                                     `ADDRESS`='{1}',
                                     `AUTHOR_ID`='{2}' 
                                 WHERE `ID`='{3}'""".format(manufacturer.name,
                                                            manufacturer.address,
                                                            manufacturer.author_id,
                                                            manufacturer_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Manufacturer with ID: {manufacturer_id} not found.'},)
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': f'Manufacturer ID {manufacturer_id} updated'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.delete('/{manufacturer_id}', status_code=status.HTTP_200_OK)
async def delete_manufacturer(manufacturer_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT `ID` FROM `manufacturers` WHERE `ID`={0}'.format(manufacturer_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = 'DELETE FROM `manufacturers` WHERE `ID`={0}'.format(manufacturer_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Manufacturer with ID: {manufacturer_id} not found.'},)
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'Manufacturer ID: {manufacturer_id} deleted'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_manufacturers():
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT * FROM `manufacturers`'
                    cursor.execute(sql)
                    result = cursor.fetchall()
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            return result
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/{manufacturer_id}', status_code=status.HTTP_200_OK, response_model=ManufacturerOut)
async def get_manufacturer(manufacturer_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT * FROM `manufacturers` WHERE `ID`={0}'.format(manufacturer_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    result = dict(result)
                    if len(result) > 0:
                        return {
                                    'id': result.get('ID'),
                                    'name': result.get('NAME'),
                                    'address': result.get('ADDRESS'),
                                    'author_id': result.get('AUTHOR_ID'),
                                    'created': result.get('CREATED'),
                                    'updated': result.get('UPDATED')
                               }
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Manufacturer with ID: {manufacturer_id} not found.'},)
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
