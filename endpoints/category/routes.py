from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import JSONResponse
import pymysql.cursors


router = APIRouter(
    prefix="/categories",
    tags=["Category"],
    responses={404: {"detail": "Not found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_category(request: Request):
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
                    sql = 'INSERT INTO `categories` (`NAME`,`AVAILABLE`,`COMMENT`,`AUTHOR_ID`) VALUES (%s,%s,%s,%s)'
                    category_name = payload.get('name') if payload.get('name') else 'Безымянная категория'
                    category_available = payload.get('available') if payload.get('available') else 0
                    category_comment = payload.get('comment') if payload.get('comment') else ''
                    category_author = payload.get('author_id') if payload.get('author_id') else 1
                    cursor.execute(sql, (category_name,
                                         category_available,
                                         category_comment,
                                         category_author))
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': 'Category added'}
    except Exception as err:
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')


@router.patch("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_category(request: Request, category_id: int):
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
                    sql = "SELECT `ID` FROM `categories` WHERE `ID`={0}".format(category_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        category_name = payload.get('name') if payload.get('name') else 'Безымянный продукт'
                        category_available = payload.get('available') if payload.get('available') else 0
                        category_comment = payload.get('comment') if payload.get('comment') else ''
                        category_author = payload.get('author_id') if payload.get('author_id') else 1
                        sql = "UPDATE `categories` SET `NAME`='{0}',`AVAILABLE`='{1}',`COMMENT`='{2}',`AUTHOR_ID`='{3}' WHERE `ID`={4}".format(
                                                                                                        category_name,
                                                                                                        category_available,
                                                                                                        category_comment,
                                                                                                        category_author,
                                                                                                        category_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Category with ID: {category_id} not found.'}, )
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': f'Category ID {category_id} updated'}
    except Exception as err:
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = "SELECT `ID` FROM `categories` WHERE `ID`={0}".format(category_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = "DELETE FROM `categories` WHERE `ID`={0}".format(category_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Category with ID: {category_id} not found.'},)
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': f'Category ID: {category_id} deleted'}
    except Exception as err:
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')


@router.get("/", status_code=status.HTTP_200_OK)
async def get_categories():
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = "SELECT * FROM `categories`"
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


@router.get("/{category_id}", status_code=status.HTTP_200_OK)
async def get_category(category_id: int):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = "SELECT * FROM `categories` WHERE `ID`={0}".format(category_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        return result
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Category with ID: {category_id} not found.'},)
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
