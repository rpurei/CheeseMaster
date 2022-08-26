from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import JSONResponse
import pymysql.cursors
import datetime


router = APIRouter(
    prefix="/orders",
    tags=["Order"],
    responses={404: {"detail": "Not found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_order(request: Request):
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
                    sql = 'INSERT INTO `orders` (`COMMENT`,`ORDER_DATE`,`STATUS`,`DELIVERY_DATE`,`PAYMENT_TYPE`,`AUTHOR_ID`) VALUES (%s,%s,%s,%s,%s,%s)'
                    order_comment = payload.get('comment') if payload.get('comment') else ''
                    order_date = payload.get('date') if payload.get('date') else datetime.datetime.now()
                    order_status = payload.get('status') if payload.get('status') else 'Неизвестен'
                    order_delivery_date = payload.get('delivery_date') if payload.get('delivery_date') else datetime.datetime.now()
                    order_payment_type = payload.get('payment_type') if payload.get('payment_type') else 'Наличными'
                    order_author = payload.get('author_id') if payload.get('author_id') else 1
                    cursor.execute(sql, (order_comment,
                                         order_date,
                                         order_status,
                                         order_delivery_date,
                                         order_payment_type,
                                         order_author
                                         ))
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': 'Order added'}
    except Exception as err:
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')


@router.patch("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_order(request: Request, order_id: int):
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
                    sql = "SELECT `ID` FROM `orders` WHERE `ID`={0}".format(order_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        order_comment = payload.get('comment') if payload.get('comment') else ''
                        order_date = payload.get('date') if payload.get('date') else datetime.datetime.now()
                        order_status = payload.get('status') if payload.get('status') else 'Неизвестен'
                        order_delivery_date = payload.get('delivery_date') if payload.get('delivery_date') else datetime.datetime.now()
                        order_payment_type = payload.get('payment_type') if payload.get('payment_type') else 'Наличными'
                        order_author = payload.get('author_id') if payload.get('author_id') else 1
                        sql = "UPDATE `orders` SET `COMMENT`='{0}',`ORDER_DATE`='{1}',`STATUS`='{2}',`DELIVERY_DATE`='{3}',`PAYMENT_TYPE`='{4}',`AUTHOR_ID`='{5}' WHERE `ID`={6}".format(
                            order_comment,
                            order_date,
                            order_status,
                            order_delivery_date,
                            order_payment_type,
                            order_author,
                            order_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Order with ID: {order_id} not found.'}, )
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': f'Order ID {order_id} updated'}
    except Exception as err:
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')


@router.delete("/{order_id}", status_code=status.HTTP_200_OK)
async def delete_order(order_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = "SELECT `ID` FROM `orders` WHERE `ID`={0}".format(order_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = "DELETE FROM `orders` WHERE `ID`={0}".format(order_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Order with ID: {order_id} not found.'},)
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': f'Order ID: {order_id} deleted'}
    except Exception as err:
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')


@router.get("/", status_code=status.HTTP_200_OK)
async def get_orders():
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = "SELECT * FROM `orders`"
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


@router.get("/{order_id}", status_code=status.HTTP_200_OK)
async def get_order(order_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = "SELECT * FROM `orders` WHERE `ID`={0}".format(order_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        return result
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Order with ID: {order_id} not found.'},)
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
