from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, IMAGE_PATH, IMAGE_NAME_LENGTH
from .models import Product
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
import pymysql.cursors
import string
import random

router = APIRouter(
    prefix="/products",
    tags=["Product"],
    responses={404: {"detail": "Not found"}},
)


def image_processing(json_image, product_category):
    image_full_name = IMAGE_PATH + 'default_product_image.png'
    print('Image', len(json_image))
    if len(json_image) > 0:
        # !!!!!!!!!!!
        # раскодировка Base64 и запись в файл
        #

        image_full_name = IMAGE_PATH + product_category + '/' + ''.join(random.choices(string.ascii_uppercase +
                                                                                          string.digits, k=IMAGE_NAME_LENGTH))

    return image_full_name


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_product(product: Product):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """INSERT INTO `products` (`NAME`,
                                                     `active`,
                                                     `CATEGORY_ID`,
                                                     `COMMENT`,
                                                     `AUTHOR_ID`,
                                                     `IMAGE_PATH`) 
                            VALUES (%s,%s,%s,%s,%s,%s)"""
                    product_image_path = image_processing(product.image_path, product.category_id)
                    cursor.execute(sql, (product.name,
                                         product.active,
                                         product.category_id,
                                         product.comment,
                                         product.author_id,
                                         product_image_path))
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': 'Product added'}
    except Exception as err:
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')


@router.patch("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_product(product: Product, product_id: int):
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
                        product_image_path = image_processing(product.image_path, product.category_id)
                        sql = """UPDATE `products` 
                                 SET `NAME`='{0}',
                                     `active`='{1}',
                                     `CATEGORY_ID`={2},
                                     `COMMENT`='{3}',
                                     `AUTHOR_ID`='{4}',
                                     `IMAGE_PATH`='{5}' 
                                 WHERE `ID`={6}""".format(product.name,
                                                            product.active,
                                                            product.category_id,
                                                            product.comment,
                                                            product.author_id,
                                                            product_image_path,
                                                            product_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Product with ID: {product_id} not found.'}, )
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
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT `ID` FROM `products` WHERE `ID`={0}'.format(product_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = 'DELETE FROM `products` WHERE `ID`={0}'.format(product_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Product with ID: {product_id} not found.'},)
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': f'Product ID: {product_id} deleted'}
    except Exception as err:
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')


@router.get("/", status_code=status.HTTP_200_OK)        #, response_model=Product
async def get_products():
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


@router.get("/{product_id}", status_code=status.HTTP_200_OK)    #, response_model=Product
async def get_product(product_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT * FROM `products` WHERE `ID`={0}'.format(product_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        return result
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Product with ID: {product_id} not found.'},)
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
