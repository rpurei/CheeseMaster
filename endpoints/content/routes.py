from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import JSONResponse
import pymysql.cursors
import datetime


router = APIRouter(
    prefix="/contents",
    tags=["Content"],
    responses={404: {"detail": "Not found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_content(request: Request):
    try:
        payload = await request.json()
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'INSERT INTO `order_contents` (`COMMENT`,`DATE`,`ORDER_ID`,`PRODUCT_ID`,`MANUFACTURER_ID`,`WAREHOUSE_ID`,`AMOUNT`,`PRICE_ID`,`STATUS`,`AUTHOR_ID`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    content_comment = payload.get('comment') if payload.get('comment') else ''
                    content_date = payload.get('date') if payload.get('date') else datetime.datetime.now()
                    content_order_id = payload.get('order_id') if payload.get('order_id') else 0
                    content_product_id = payload.get('product_id') if payload.get('product_id') else 1
                    content_manufacturer_id = payload.get('manufacturer_id') if payload.get('manufacturer_id') else 1
                    content_warehouse_id = payload.get('warehouse_id') if payload.get('warehouse_id') else 1
                    content_amount = payload.get('amount') if payload.get('amount') else 0
                    content_price_id = payload.get('price_id') if payload.get('price_id') else 1
                    content_status = payload.get('status') if payload.get('status') else ''
                    content_author = payload.get('author_id') if payload.get('author_id') else 1
                    cursor.execute(sql, (content_comment,
                                         content_date,
                                         content_order_id,
                                         content_product_id,
                                         content_manufacturer_id,
                                         content_warehouse_id,
                                         content_amount,
                                         content_price_id,
                                         content_status,
                                         content_author
                                         ))
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': 'Content added'}
    except Exception as err:
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')


@router.patch("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_content(request: Request, content_id: int):
    try:
        payload = await request.json()
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = "SELECT `ID` FROM `order_contents` WHERE `ID`={0}".format(content_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        content_comment = payload.get('comment') if payload.get('comment') else ''
                        content_date = payload.get('date') if payload.get('date') else datetime.datetime.now()
                        content_order_id = payload.get('order_id') if payload.get('order_id') else 0
                        content_product_id = payload.get('product_id') if payload.get('product_id') else 1
                        content_manufacturer_id = payload.get('manufacturer_id') if payload.get('manufacturer_id') else 1
                        content_warehouse_id = payload.get('warehouse_id') if payload.get('warehouse_id') else 1
                        content_amount = payload.get('amount') if payload.get('amount') else 0
                        content_price_id = payload.get('price_id') if payload.get('price_id') else 1
                        content_status = payload.get('status') if payload.get('status') else ''
                        content_author = payload.get('author_id') if payload.get('author_id') else 1
                        sql = "UPDATE `order_contents` SET `COMMENT`='{0}',`DATE`='{1}',`ORDER_ID`='{2}',`PRODUCT_ID`='{3}',`MANUFACTURER_ID`='{4}',`WAREHOUSE_ID`='{5}',`AMOUNT`='{6}',`PRICE_ID`='{7}',`STATUS`='{8}',`AUTHOR_ID`='{9}' WHERE `ID`={10}".format(
                            content_comment,
                            content_date,
                            content_order_id,
                            content_product_id,
                            content_manufacturer_id,
                            content_warehouse_id,
                            content_amount,
                            content_price_id,
                            content_status,
                            content_author,
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
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': f'Content ID {content_id} updated'}
    except Exception as err:
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')


@router.delete("/{content_id}", status_code=status.HTTP_200_OK)
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
                    sql = "SELECT `ID` FROM `order_contents` WHERE `ID`={0}".format(content_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = "DELETE FROM `order_contents` WHERE `ID`={0}".format(content_id)
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
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')


@router.get("/", status_code=status.HTTP_200_OK)
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
                    sql = "SELECT * FROM `order_contents`"
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


@router.get("/{content_id}", status_code=status.HTTP_200_OK)
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
                    sql = "SELECT * FROM `order_contents` WHERE `ID`={0}".format(content_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        return result
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
    except Exception as err:
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')
