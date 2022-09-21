from app_logger import logger
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from .models import ProductionIn, ProductionOut
from ..users.utils import get_current_user
from fastapi import APIRouter, status, HTTPException, Security
from fastapi.responses import JSONResponse
import pymysql.cursors
import traceback

router = APIRouter(
    prefix='/productions',
    tags=['Production'],
    responses={404: {'detail': 'Not found'}},
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_production(production: ProductionIn,
                         current_user=Security(get_current_user, scopes=['production:create'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """INSERT INTO `productions` (`product_id`,
                                                        `manufacturer_id`,
                                                        `storage_id`,
                                                        `amount`,
                                                        `item_measure`,
                                                        `date`,
                                                        `operation`,
                                                        `comment`,
                                                        `author_id`) 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(sql, (production.product_id,
                                         production.manufacturer_id,
                                         production.storage_id,
                                         production.amount,
                                         production.item_measure,
                                         production.date,
                                         production.operation,
                                         production.comment,
                                         production.author_id
                                         ))
                    sql = """SELECT `id`,`amount` FROM `warehouses` 
                             WHERE `storage_id`='{0}' AND `product_id`='{1}'""".format(production.storage_id,
                                                                                       production.product_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    result = dict(result)
                    record_id = result.get('id')
                    current_amount = float(result.get('amount'))
                    if result:
                        amount = current_amount + production.amount
                        sql = """UPDATE `warehouses` SET `amount`='{0}'
                                 WHERE `id`='{1}'""".format(amount, record_id)
                        cursor.execute(sql)
                    else:
                        sql = """INSERT INTO `warehouses` (`storage_id`,
                                                           `product_id`,
                                                           `amount`,
                                                           `item_measure`,
                                                           `active`,
                                                           `author_id`)
                                 VALUES (%s,%s,%s,%s,%s,%s)""".format(production.storage_id,
                                                                      production.product_id,
                                                                      production.amount,
                                                                      production.item_measure,
                                                                      1,
                                                                      production.author_id)
                        cursor.execute(sql)
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': 'Production added'}
    except Exception as err:
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")} : {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'{traceback.format_exc()} : {str(err)}')


@router.patch('/{production_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_production(production: ProductionIn, production_id: int,
                            current_user=Security(get_current_user, scopes=['production:update'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT `ID`,`amount` FROM `productions` WHERE `ID`={0}'.format(production_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    result = dict(result)
                    old_amount = result.get('amount')
                    if result:
                        sql = """UPDATE `productions` 
                                 SET `product_id`='{0}',
                                     `manufacturer_id`='{1}',
                                     `storage_id`='{2}',
                                     `amount`='{3}',
                                     `item_measure`='{4}',
                                     `date`='{5}',
                                     `comment`='{6}',
                                     `author_id`='{7}' 
                                 WHERE `id`='{8}'""".format(production.product_id,
                                                            production.manufacturer_id,
                                                            production.storage_id,
                                                            production.amount,
                                                            production.item_measure,
                                                            production.date,
                                                            production.comment,
                                                            production.author_id,
                                                            production_id)
                        cursor.execute(sql)
                        ########################
                        sql = """SELECT `id`,`amount` FROM `warehouses` 
                                 WHERE `storage_id`='{0}' AND `product_id`='{1}'""".format(production.storage_id,
                                                                                           production.product_id)
                        cursor.execute(sql)
                        result = cursor.fetchone()
                        result = dict(result)
                        record_id = result.get('id')
                        current_amount = float(result.get('amount'))
                        if result:
                            amount = current_amount - old_amount + production.amount
                            sql = """UPDATE `warehouses` SET `amount`='{0}'
                                     WHERE `id`='{1}'""".format(amount, record_id)
                            cursor.execute(sql)
                        else:
                            sql = """INSERT INTO `warehouses` (`storage_id`,
                                                               `product_id`,
                                                               `amount`,
                                                               `item_measure`,
                                                               `active`,
                                                               `author_id`)
                                     VALUES (%s,%s,%s,%s,%s,%s)""".format(production.storage_id,
                                                                          production.product_id,
                                                                          production.amount,
                                                                          production.item_measure,
                                                                          1,
                                                                          production.author_id)
                            cursor.execute(sql)
                        ########################
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Production with ID: {production_id} not found.'}, )
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'Production ID {production_id} updated'}
    except Exception as err:
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")} : {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'{traceback.format_exc()} : {str(err)}')


@router.delete('/{production_id}', status_code=status.HTTP_200_OK)
async def delete_production(production_id: int, current_user=Security(get_current_user, scopes=['superadmin'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT `id` FROM `productions` WHERE `id`='{0}'""".format(production_id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        sql = """DELETE FROM `productions` WHERE `id`='{0}'""".format(production_id)
                        cursor.execute(sql)
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Production with ID: {production_id} not found.'},)
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            connection.commit()
            return {'detail': f'Production ID: {production_id} deleted'}
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_productions(current_user=Security(get_current_user, scopes=['production:read'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = 'SELECT * FROM `productions`'
                    cursor.execute(sql)
                    result = cursor.fetchall()
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
            return result
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')


@router.get('/{production_id}', status_code=status.HTTP_200_OK, response_model=ProductionOut)
async def get_production(production_id: int, current_user=Security(get_current_user, scopes=['production:read'])):
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT * FROM `productions` WHERE `id`='{0}'""".format(production_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    result = dict(result)
                    if result:
                        return {'id': result.get('id'),
                                'date': result.get('date'),
                                'product_id': result.get('product_id'),
                                'manufacturer_id': result.get('manufacturer_id'),
                                'storage_id': result.get('storage_id'),
                                'amount': result.get('amount'),
                                'item_measure': result.get('item_measure'),
                                'operation': result.get('operation'),
                                'comment': result.get('comment'),
                                'author_id': result.get('author_id'),
                                'created': result.get('created'),
                                'updated': result.get('updated')}
                    else:
                        return JSONResponse(status_code=404,
                                            content={'detail': f'Production with ID: {production_id} not found.'},)
                except Exception as err:
                    logger.error(f'Error: {str(err)}')
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
    except Exception as err:
        logger.error(f'Error: {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error {str(err)}')
