from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from .models import ContentIn, ContentOut
from ..users.utils import get_current_user
from fastapi import APIRouter, status, HTTPException, Security
from fastapi.responses import JSONResponse
import pymysql.cursors

router = APIRouter(
    prefix='/contents',
    tags=['Content'],
    responses={404: {'detail': 'Not found'}},
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_content(content: ContentIn, current_user=Security(get_current_user, scopes=['content:create'])):
    print(current_user)
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
                                        (`comment`,
                                        `date`,
                                        `order_id`,
                                        `product_id`,
                                        `manufacturer_id`,
                                        `storage_id`,
                                        `amount`,
                                        `price_id`,
                                        `status`,
                                        `author_id`) 
                             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(sql, (content.comment,
                                         content.date,
                                         content.order_id,
                                         content.product_id,
                                         content.manufacturer_id,
                                         content.storage_id,
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
async def update_content(content: ContentIn, content_id: int,
                         current_user=Security(get_current_user, scopes=['content:update'])):
    logger.info(f'User: {current_user}')
    print(current_user)
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
                    if result:
                        sql = """UPDATE `order_contents` 
                                 SET `comment`='{0}',
                                     `date`='{1}',
                                     `order_id`='{2}',
                                     `product_id`='{3}',
                                     `manufacturer_id`='{4}',
                                     `storage_id`='{5}',
                                     `amount`='{6}',
                                     `price_id`='{7}',
                                     `status`='{8}',
                                     `author_id`='{9}' 
                                 WHERE `id`='{10}'""".format(
                            content.comment,
                            content.date,
                            content.order_id,
                            content.product_id,
                            content.manufacturer_id,
                            content.storage_id,
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
async def delete_content(content_id: int, current_user=Security(get_current_user, scopes=['content:delete'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT `ID` FROM `order_contents` WHERE `id`='{0}'""".format(content_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        sql = """DELETE FROM `order_contents` WHERE `id`='{0}'""".format(content_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Content with ID: {content_id} not found.'}, )
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
async def get_contents(current_user=Security(get_current_user, scopes=['content:read'])):
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
async def get_content(content_id: int, current_user=Security(get_current_user, scopes=['content:read'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT * FROM `order_contents` WHERE `id`='{0}'""".format(content_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    result = dict(result)
                    if result:
                        return {'id': result.get('id'),
                                'date': result.get('date'),
                                'order_id': result.get('order_id'),
                                'product_id': result.get('product_id'),
                                'manufacturer_id': result.get('manufacturer_id'),
                                'storage_id': result.get('storage_id'),
                                'amount': result.get('amount'),
                                'price_id': result.get('price_id'),
                                'status': result.get('status'),
                                'comment': result.get('comment'),
                                'author_id': result.get('author_id'),
                                'created': result.get('created'),
                                'updated': result.get('updated')}
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Content with ID: {content_id} not found.'}, )
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
