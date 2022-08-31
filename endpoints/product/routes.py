from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, IMAGE_PATH, IMAGE_NAME_LENGTH
from .models import ProductIn, ProductOut
from .utils import image_processing
from ..users.utils import get_current_user
from fastapi import APIRouter, status, HTTPException, Security
from fastapi.responses import JSONResponse
import pymysql.cursors


router = APIRouter(
    prefix='/products',
    tags=['Product'],
    responses={404: {'detail': 'Not found'}},
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_product(product: ProductIn, current_user=Security(get_current_user, scopes=['admin'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """INSERT INTO `products` (`name`,
                                                     `active`,
                                                     `category_id`,
                                                     `description`,
                                                     `comment`,
                                                     `author_id`,
                                                     `image_path`) 
                             VALUES (%s,%s,%s,%s,%s,%s,%s)"""
                    product_image_path = image_processing(product.image, product.category_id, product.ext)
                    cursor.execute(sql, (product.name,
                                         product.active,
                                         product.category_id,
                                         product.description,
                                         product.comment,
                                         product.author_id,
                                         str(product_image_path)))
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': 'Product added'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.patch('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_product(product: ProductIn, product_id: int, current_user=Security(get_current_user, scopes=['admin'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = "SELECT `ID` FROM `products` WHERE `ID`={0}".format(product_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        product_image_path = image_processing(product.image, product.category_id, product.ext)
                        sql = """UPDATE `products` 
                                 SET `name`='{0}',
                                     `active`='{1}',
                                     `category_id`='{2}',
                                     `description`='{3}',
                                     `comment`='{4}',
                                     `author_id`='{5}',
                                     `image_path`='{6}' 
                                 WHERE `id`='{7}'""".format(product.name,
                                                          product.active,
                                                          product.category_id,
                                                          product.description,
                                                          product.comment,
                                                          product.author_id,
                                                          product_image_path,
                                                          product_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Product with ID: {product_id} not found.'}, )
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': f'Product ID: {product_id} updated'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.delete('/{product_id}', status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, current_user=Security(get_current_user,scopes=['superadmin'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT `id` FROM `products` WHERE `id`='{0}'""".format(product_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = """DELETE FROM `products` WHERE `id`='{0}'""".format(product_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Product with ID: {product_id} not found.'}, )
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'Product ID: {product_id} deleted'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_products(current_user=Security(get_current_user, scopes=['admin', 'user:read', 'cheesemaster:read'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT * FROM `products`'
                    cursor.execute(sql)
                    result = cursor.fetchall()
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            return result
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/{product_id}', status_code=status.HTTP_200_OK, response_model=ProductOut)
async def get_product(product_id: int, current_user=Security(get_current_user, scopes=['admin',
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
                    sql = """SELECT * FROM `products` WHERE `id`='{0}'""".format(product_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    result = dict(result)
                    if len(result) > 0:
                        return {
                                    'id': result.get('id'),
                                    'name': result.get('name'),
                                    'active': result.get('active'),
                                    'category_id': result.get('category_id'),
                                    'comment': result.get('comment'),
                                    'description': result.get('description'),
                                    'author_id': result.get('author_id'),
                                    'image_path': result.get('image_path'),
                                    'created': result.get('created'),
                                    'updated': result.get('updated')
                               }
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Product with ID: {product_id} not found.'}, )
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)}')
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
