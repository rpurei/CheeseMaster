from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from .models import ContentIn, ContentOut
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
import pymysql.cursors


router = APIRouter(
    prefix='/contents',
    tags=['Content'],
    responses={404: {'detail': 'Not found'}},
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_content(content: ContentIn):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """INSERT INTO `order_contents` 
                                        (`COMMENT`,
                                        `DATE`,
                                        `ORDER_ID`,
                                        `PRODUCT_ID`,
                                        `MANUFACTURER_ID`,
                                        `WAREHOUSE_ID`,
                                        `AMOUNT`,
                                        `PRICE_ID`,
                                        `STATUS`,
                                        `AUTHOR_ID`) 
                             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(sql, (content.comment,
                                         content.date,
                                         content.order_id,
                                         content.product_id,
                                         content.manufacturer_id,
                                         content.warehouse_id,
                                         content.amount,
                                         content.price_id,
                                         content.status,
                                         content.author_id
                                         ))
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': 'Content added'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.patch('/{content_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_content(content: ContentIn, content_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT `ID` FROM `order_contents` WHERE `ID`={0}'.format(content_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = """UPDATE `order_contents` 
                                 SET `COMMENT`='{0}',
                                     `DATE`='{1}',
                                     `ORDER_ID`='{2}',
                                     `PRODUCT_ID`='{3}',
                                     `MANUFACTURER_ID`='{4}',
                                     `WAREHOUSE_ID`='{5}',
                                     `AMOUNT`='{6}',
                                     `PRICE_ID`='{7}',
                                     `STATUS`='{8}',
                                     `AUTHOR_ID`='{9}' 
                                 WHERE `ID`={10}""".format(
                            content.comment,
                            content.date,
                            content.order_id,
                            content.product_id,
                            content.manufacturer_id,
                            content.warehouse_id,
                            content.amount,
                            content.price_id,
                            content.status,
                            content.author_id,
                            content_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Content with ID: {content_id} not found.'}, )
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'Content ID {content_id} updated'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.delete('/{content_id}', status_code=status.HTTP_200_OK)
async def delete_content(content_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT `ID` FROM `order_contents` WHERE `ID`={0}'.format(content_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = 'DELETE FROM `order_contents` WHERE `ID`={0}'.format(content_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Content with ID: {content_id} not found.'},)
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': f'Content ID: {content_id} deleted'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_contents():
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT * FROM `order_contents`'
                    cursor.execute(sql)
                    result = cursor.fetchall()
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            return result
    except Exception as err:
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')


@router.get("/{content_id}", status_code=status.HTTP_200_OK, response_model=ContentOut)
async def get_content(content_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT * FROM `order_contents` WHERE `ID`={0}'.format(content_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    result = dict(result)
                    if len(result) > 0:
                        return {'id': result.get('ID'),
                                'date': result.get('DATE'),
                                'order_id': result.get('ORDER_ID'),
                                'product_id': result.get('PRODUCT_ID'),
                                'manufacturer_id': result.get('MANUFACTURER_ID'),
                                'warehouse_id': result.get('WAREHOUSE_ID'),
                                'amount': result.get('AMOUNT'),
                                'price_id': result.get('PRICE_ID'),
                                'status': result.get('STATUS'),
                                'comment': result.get('COMMENT'),
                                'author_id': result.get('AUTHOR_ID'),
                                'created': result.get('CREATED'),
                                'updated': result.get('UPDATED')}
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Content with ID: {content_id} not found.'},)
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
