from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from .models import OrderIn, OrderOut, OrderContentOut
from ..users.utils import get_current_user
from ..product.routes import get_product_by_id
from ..manufacturer.routes import get_manufacturer_by_id
from ..storage.routes import get_storage_by_id
from ..price.routes import get_price_by_id
from fastapi import APIRouter, status, HTTPException, Security
from fastapi.responses import JSONResponse
import pymysql.cursors
import traceback

router = APIRouter(
    prefix='/orders',
    tags=['Order'],
    responses={404: {'detail': 'Not found'}},
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_order(order: OrderIn, current_user=Security(get_current_user, scopes=['order:create'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """INSERT INTO `orders` (`user_id`,
                                                   `comment`,
                                                   `order_date`,
                                                   `status`,
                                                   `delivery_date`,
                                                   `payment_type`,
                                                   `pickpoint_id`,
                                                   `author_id`) 
                             VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(sql, (order.user_id,
                                         order.comment,
                                         order.date,
                                         order.status,
                                         order.delivery_date,
                                         order.payment_type,
                                         order.pickpoint_id,
                                         order.author_id
                                         ))
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'{cursor.lastrowid} order added'}
    except Exception as err:
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")} : {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'{traceback.format_exc()} : {str(err)}')


@router.patch('/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_order(order: OrderIn, order_id: int, current_user=Security(get_current_user, scopes=['order:update'])):
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
                    if result:
                        sql = """UPDATE `orders` 
                                 SET 
                                 `comment`='{0}',
                                 `order_date`='{1}',
                                 `status`='{2}',
                                 `delivery_date`='{3}',
                                 `payment_type`='{4}',
                                 `pickpoint_id`='{5}',
                                 `author_id`='{6}' 
                                 WHERE `id`='{7}'""".format(order.comment,
                                                            order.date,
                                                            order.status,
                                                            order.delivery_date,
                                                            order.payment_type,
                                                            order.pickpoint_id,
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
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")} : {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'{traceback.format_exc()} : {str(err)}')


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
                    if result:
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
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")} : {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'{traceback.format_exc()} : {str(err)}')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_orders(current_user=Security(get_current_user, scopes=['order:read'])):
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
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")} : {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'{traceback.format_exc()} : {str(err)}')


@router.get('/{order_id}', status_code=status.HTTP_200_OK, response_model=OrderOut)
async def get_order(order_id: int, current_user=Security(get_current_user, scopes=['order:read'])):
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
                    if result:
                        return {
                            'id': result.get('id'),
                            'user_id': result.get('user_id'),
                            'date': result.get('order_date'),
                            'delivery_date': result.get('delivery_date'),
                            'payment_type': result.get('payment_type'),
                            'status': result.get('status'),
                            'pickpoint_id': result.get('pickpoint_id'),
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
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")} : {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'{traceback.format_exc()} : {str(err)}')


@router.get('/{order_id}/content', status_code=status.HTTP_200_OK, response_model=OrderContentOut)
async def get_order_content(order_id: int, current_user=Security(get_current_user, scopes=['order:read'])):
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
                    sql = """SELECT * FROM `order_contents` WHERE `order_id`='{0}'""".format(order_id)
                    cursor.execute(sql)
                    result_content = cursor.fetchall()
                    content_list = []
                    for content in result_content:
                        content = dict(content)
                        dct = {
                                'id': content.get('id'),
                                'date': content.get('date'),
                                'order_id': content.get('order_id'),
                                'product': get_product_by_id(content.get('product_id')),
                                'manufacturer': get_manufacturer_by_id(content.get('manufacturer_id')),
                                'storage': get_storage_by_id(content.get('storage_id')),
                                'amount': content.get('amount'),
                                'price': get_price_by_id(content.get('price_id')),
                                'status': content.get('status'),
                                'comment': content.get('comment'),
                                'author_id': content.get('author_id'),
                                'created': content.get('created'),
                                'updated': content.get('updated')
                              }
                        content_list.append(dct)
                    if result:
                        result = dict(result)
                        return {
                                'id': result.get('id'),
                                'user_id': result.get('user_id'),
                                'date': result.get('order_date'),
                                'delivery_date': result.get('delivery_date'),
                                'payment_type': result.get('payment_type'),
                                'status': result.get('status'),
                                'pickpoint_id': result.get('pickpoint_id'),
                                'comment': result.get('comment'),
                                'author_id': result.get('author_id'),
                                'created': result.get('created'),
                                'updated': result.get('updated'),
                                'content': content_list
                               }
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Order with ID: {order_id} not found.'}, )
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
    except Exception as err:
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")} : {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'{traceback.format_exc()} : {str(err)}')