from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import JSONResponse
import pymysql.cursors


router = APIRouter(
    prefix="/prices",
    tags=["Price"],
    responses={404: {"detail": "Not found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_price(request: Request):
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
                    sql = 'INSERT INTO `prices` (`PRODUCT_ID`,`ITEM_MEASURE`,`ITEM_PRICE`,`AUTHOR_ID`) VALUES (%s,%s,%s,%s)'
                    price_product_id = payload.get('product_id') if payload.get('product_id') else 1
                    price_item_measure = payload.get('item_measure') if payload.get('item_measure') else 'кг'
                    price_item_price = payload.get('item_price') if payload.get('item_price') else 0
                    price_author = payload.get('author_id') if payload.get('author_id') else 1
                    cursor.execute(sql, (price_product_id,
                                         price_item_measure,
                                         price_item_price,
                                         price_author
                                         ))
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': 'Price added'}
    except Exception as err:
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')


@router.patch("/{price_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_price(request: Request, price_id: int):
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
                    sql = "SELECT `ID` FROM `prices` WHERE `ID`={0}".format(price_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        price_product_id = payload.get('product_id') if payload.get('product_id') else 1
                        price_item_measure = payload.get('item_measure') if payload.get('item_measure') else 'кг'
                        price_item_price = payload.get('item_price') if payload.get('item_price') else 0
                        price_author = payload.get('author_id') if payload.get('author_id') else 1
                        sql = "UPDATE `prices` SET `PRODUCT_ID`='{0}',`ITEM_MEASURE`='{1}',`ITEM_PRICE`='{2}',`AUTHOR_ID`='{3}' WHERE `ID`={4}".format(
                                                                                                        price_product_id,
                                                                                                        price_item_measure,
                                                                                                        price_item_price,
                                                                                                        price_author,
                                                                                                        price_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Price with ID: {price_id} not found.'}, )
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': f'Price ID {price_id} updated'}
    except Exception as err:
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')


@router.delete("/{price_id}", status_code=status.HTTP_200_OK)
async def delete_price(price_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = "SELECT `ID` FROM `prices` WHERE `ID`={0}".format(price_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = "DELETE FROM `prices` WHERE `ID`={0}".format(price_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Price with ID: {price_id} not found.'},)
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': f'Price ID: {price_id} deleted'}
    except Exception as err:
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')


@router.get("/", status_code=status.HTTP_200_OK)
async def get_prices():
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = "SELECT * FROM `prices`"
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


@router.get("/{price_id}", status_code=status.HTTP_200_OK)
async def get_price(price_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = "SELECT * FROM `prices` WHERE `ID`={0}".format(price_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        return result
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Price with ID: {price_id} not found.'},)
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
