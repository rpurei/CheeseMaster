from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from .models import ProductionIn, ProductionOut
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
import pymysql.cursors


router = APIRouter(
    prefix='/productions',
    tags=['Production'],
    responses={404: {'detail': 'Not found'}},
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_production(production: ProductionIn):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """INSERT INTO `productions` (`PRODUCT_ID`,
                                                        `MANUFACTURER_ID`,
                                                        `WAREHOUSE_ID`,
                                                        `AMOUNT`,
                                                        `ITEM_MEASURE`,
                                                        `DATE`,
                                                        `COMMENT`,
                                                        `AUTHOR_ID`) 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(sql, (production.product_id,
                                         production.manufacturer_id,
                                         production.warehouse_id,
                                         production.amount,
                                         production.date,
                                         production.comment,
                                         production.author_id
                                         ))
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': 'Production added'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.patch('/{production_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_production(production: ProductionIn, production_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT `ID` FROM `productions` WHERE `ID`={0}'.format(production_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = """UPDATE `productions` 
                                 SET `PRODUCT_ID`='{0}',
                                     `MANUFACTURER_ID`='{1}',
                                     `WAREHOUSE_ID`='{2}',
                                     `AMOUNT`='{3}',
                                     `ITEM_MEASURE`='{4}',
                                     `DATE`='{5}',
                                     `COMMENT`='{6}',
                                     `AUTHOR_ID`='{7}' 
                                 WHERE `ID`={8}""".format(production.product_id,
                                                            production.manufacturer_id,
                                                            production.warehouse_id,
                                                            production.amount,
                                                            production.item_measure,
                                                            production.date,
                                                            production.comment,
                                                            production.author_id,
                                                            production_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Production with ID: {production_id} not found.'}, )
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'Production ID {production_id} updated'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.delete('/{production_id}', status_code=status.HTTP_200_OK)
async def delete_production(production_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT `ID` FROM `productions` WHERE `ID`={0}'.format(production_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = 'DELETE FROM `productions` WHERE `ID`={0}'.format(production_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Production with ID: {production_id} not found.'},)
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'Production ID: {production_id} deleted'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_productions():
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT * FROM `productions`'
                    cursor.execute(sql)
                    result = cursor.fetchall()
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            return result
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/{production_id}', status_code=status.HTTP_200_OK, response_model=ProductionOut)
async def get_production(production_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT * FROM `productions` WHERE `ID`={0}'.format(production_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    result = dict(result)
                    if len(result) > 0:
                        return {'id': result.get('ID'),
                                'date': result.get('DATE'),
                                'product_id': result.get('PRODUCT_ID'),
                                'manufacturer_id': result.get('MANUFACTURER_ID'),
                                'warehouse_id': result.get('WAREHOUSE_ID'),
                                'amount': result.get('AMOUNT'),
                                'item_measure': result.get('ITEM_MEASURE'),
                                'comment': result.get('COMMENT'),
                                'author_id': result.get('AUTHOR_ID'),
                                'created': result.get('CREATED'),
                                'updated': result.get('UPDATED')}
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Production with ID: {production_id} not found.'},)
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
