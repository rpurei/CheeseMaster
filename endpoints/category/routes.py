from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from .models import CategoryIn, CategoryOut
from ..users.utils import get_current_user
from fastapi import APIRouter, status, HTTPException, Depends, Security
from fastapi.responses import JSONResponse
import pymysql.cursors


router = APIRouter(
    prefix='/categories',
    tags=['Category'],
    responses={404: {'detail': 'Not found'}},
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_category(category: CategoryIn):               #, current_user=Security(get_current_user, scopes=['admin'])
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """INSERT INTO `categories` 
                                         (`name`,
                                         `active`,
                                         `comment`,
                                         `author_id`) 
                             VALUES (%s,%s,%s,%s)"""
                    cursor.execute(sql, (category.name,
                                         category.active,
                                         category.comment,
                                         category.author_id))
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': 'Category added'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.patch('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_category(category: CategoryIn, category_id: int):                  #, current_user=Security(get_current_user,
                                                                                    #    scopes=['admin'])
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT `ID` FROM `categories` WHERE `ID`={0}'.format(category_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = """UPDATE `categories` 
                                 SET `name`='{0}',
                                     `active`='{1}',
                                     `comment`='{2}',
                                     `author_id`='{3}' 
                                 WHERE `id`='{4}'""".format(category.name,
                                                            category.active,
                                                            category.comment,
                                                            category.author_id,
                                                            category_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Category with ID: {category_id} not found.'}, )
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'Category ID {category_id} updated'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.delete('/{category_id}', status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, current_user=Security(get_current_user,scopes=['superadmin'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT `ID` FROM `categories` WHERE `id`='{0}'""".format(category_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = """DELETE FROM `categories` WHERE `id`='{0}'""".format(category_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Category with ID: {category_id} not found.'},)
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'Category ID: {category_id} deleted'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get("/", status_code=status.HTTP_200_OK)
async def get_categories():                                 #current_user=Security(get_current_user, scopes=['admin', 'user:read', 'cheesemaster:read'])
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT * FROM `categories`'
                    cursor.execute(sql)
                    result = cursor.fetchall()
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)}')
            return result
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/{category_id}', status_code=status.HTTP_200_OK, response_model=CategoryOut)
async def get_category(category_id: int):                                   #, current_user=Security(get_current_user, scopes=['admin',
                                                                            #             'user:read',
                                                                            #             'cheesemaster:read'])
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT * FROM `categories` WHERE `id`='{0}'""".format(category_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    result = dict(result)
                    if len(result) > 0:
                        return {'id': result.get('id'),
                                'name': result.get('name'),
                                'active': result.get('active'),
                                'comment': result.get('comment'),
                                'author_id': result.get('author_id'),
                                'created': result.get('created'),
                                'updated': result.get('updated')
                                }
                    else:
                        return JSONResponse(status_code=404,
                                            content={"detail": f'Category with ID: {category_id} not found.'},)
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
