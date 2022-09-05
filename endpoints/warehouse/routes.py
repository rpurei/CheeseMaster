from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from .models import WarehouseIn, WarehouseOut
from ..users.utils import get_current_user
from fastapi import APIRouter, status, HTTPException, Security
from fastapi.responses import JSONResponse
import pymysql.cursors


router = APIRouter(
    prefix='/warehouses',
    tags=['Warehouse'],
    responses={404: {'detail': 'Not found'}},
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_warehouse(warehouse: WarehouseIn):
    # , current_user = Security(get_current_user, scopes=['admin'])
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """INSERT INTO `warehouses` (`product_id`,
                                                       `amount`,
                                                       `item_measure`,
                                                       `reserve`,
                                                       `active`,
                                                       `author_id`) 
                             VALUES (%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(sql, (warehouse.product_id,
                                         warehouse.amount,
                                         warehouse.item_measure,
                                         warehouse.reserve,
                                         warehouse.active,
                                         warehouse.author_id
                                         ))
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': 'Warehouse added'}
    except Exception as err:
        err_message = ''
        for err_item in err.args:
            err_message += err_item
        logger.error(f'Error: {str(err)} {err_message}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)} {err_message}')


@router.patch('/{warehouse_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_warehouse(warehouse: WarehouseIn, warehouse_id: int):
    # , current_user = Security(get_current_user,
    #                           scopes=['admin'])
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT `ID` FROM `warehouses` WHERE `ID`={0}'.format(warehouse_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = """UPDATE `warehouses` 
                                 SET `product_id`='{0}',
                                     `amount`='{1}',
                                     `item_measure`='{2}',
                                     `reserve`='{3}',
                                     `active`='{4}',
                                     `author_id`='{5}' 
                                 WHERE `id`='{6}'""".format(warehouse.product_id,
                                                          warehouse.amount,
                                                          warehouse.item_measure,
                                                          warehouse.reserve,
                                                          warehouse.active,
                                                          warehouse.author_id,
                                                          warehouse_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Warehouse with ID: {warehouse_id} not found.'}, )
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail=f'Error {str(err)} {err_message}')
            connection.commit()
            return {'detail': f'Warehouse ID {warehouse_id} updated'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.delete("/{warehouse_id}", status_code=status.HTTP_200_OK)
async def delete_warehouse(warehouse_id: int):
    # , current_user = Security(get_current_user, scopes=['superadmin'])
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT `id` FROM `warehouses` WHERE `id`='{0}'""".format(warehouse_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        sql = """DELETE FROM `warehouses` WHERE `id`='{0}'""".format(warehouse_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Warehouse with ID: {warehouse_id} not found.'},)
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'Warehouse ID: {warehouse_id} deleted'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_warehouses():
    # current_user = Security(get_current_user, scopes=['admin', 'cheesemaster:read'])
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT * FROM `warehouses`'
                    cursor.execute(sql)
                    result = cursor.fetchall()
                except Exception as err:
                    err_message = ''
                    for err_item in err.args:
                        err_message += err_item
                    logger.error(f'Error: {str(err)} {err_message}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            return result
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/{warehouse_id}', status_code=status.HTTP_200_OK, response_model=WarehouseOut)
async def get_warehouse(warehouse_id: int):
    # , current_user = Security(get_current_user, scopes=['admin',
    #                                                     'cheesemaster:read'])
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT * FROM `warehouses` WHERE `id`='{0}'""".format(warehouse_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    result = dict(result)
                    if len(result) > 0:
                        return {
                                    'id': result.get('id'),
                                    'product_id': result.get('product_id'),
                                    'amount': result.get('amount'),
                                    'item_measure': result.get('item_measure'),
                                    'reserve': result.get('reserve'),
                                    'active': result.get('active'),
                                    'author_id': result.get('author_id'),
                                    'created': result.get('created'),
                                    'updated': result.get('updated')
                        }
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Warehouse with ID: {warehouse_id} not found.'},)
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
