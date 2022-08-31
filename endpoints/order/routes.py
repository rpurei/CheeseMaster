from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from .models import OrderIn, OrderOut
from ..users.utils import get_current_user
from fastapi import APIRouter, status, HTTPException, Security
from fastapi.responses import JSONResponse
import pymysql.cursors

router = APIRouter(
    prefix='/orders',
    tags=['Order'],
    responses={404: {'detail': 'Not found'}},
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_order(order: OrderIn, current_user=Security(get_current_user, scopes=['admin',
                                                                                    'user:create',
                                                                                    'cheesemaster:create'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """INSERT INTO `orders` (`comment`,
                                                   `order_date`,
                                                   `status`,
                                                   `delivery_date`,
                                                   `payment_type`,
                                                   `author_id`) 
                             VALUES (%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(sql, (order.comment,
                                         order.date,
                                         order.status,
                                         order.delivery_date,
                                         order.payment_type,
                                         order.author_id
                                         ))
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': 'Order added'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.patch('/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_order(order: OrderIn, order_id: int, current_user=Security(get_current_user,
                                                                            scopes=['admin',
                                                                                    'user:update',
                                                                                    'cheesemaster:update'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = "SELECT `id` FROM `orders` WHERE `id`={0}".format(order_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = """UPDATE `orders` 
                                 SET 
                                 `comment`='{0}',
                                 `order_date`='{1}',
                                 `status`='{2}',
                                 `delivery_date`='{3}',
                                 `payment_type`='{4}',
                                 `author_id`='{5}' 
                                 WHERE `id`='{6}'""".format(order.comment,
                                                            order.date,
                                                            order.status,
                                                            order.delivery_date,
                                                            order.payment_type,
                                                            order.author_id,
                                                            order_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Order with ID: {order_id} not found.'}, )
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'Order ID {order_id} updated'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.delete('/{order_id}', status_code=status.HTTP_200_OK)
async def delete_order(order_id: int, current_user=Security(get_current_user, scopes=['superadmin'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT `ID` FROM `orders` WHERE `id`='{0}'""".format(order_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = """DELETE FROM `orders` WHERE `id`='{0}'""".format(order_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Order with ID: {order_id} not found.'}, )
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'Order ID: {order_id} deleted'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_orders(current_user=Security(get_current_user, scopes=['admin',
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
                    sql = 'SELECT * FROM `orders`'
                    cursor.execute(sql)
                    result = cursor.fetchall()
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            return result
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/{order_id}', status_code=status.HTTP_200_OK, response_model=OrderOut)
async def get_order(order_id: int, current_user=Security(get_current_user, scopes=['admin',
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
                    sql = """SELECT * FROM `orders` WHERE `id`='{0}'""".format(order_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    result = dict(result)
                    if len(result) > 0:
                        return {
                            'id': result.get('id'),
                            'date': result.get('order_date'),
                            'delivery_date': result.get('delivery_date'),
                            'payment_type': result.get('payment_type'),
                            'status': result.get('status'),
                            'comment': result.get('comment'),
                            'author_id': result.get('author_id'),
                            'created': result.get('created'),
                            'updated': result.get('updated')
                        }
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Order with ID: {order_id} not found.'}, )
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
