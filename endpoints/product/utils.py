from app_logger import logger
from config import IMAGE_PATH, IMAGE_NAME_LENGTH
import string
import random
import base64
from pathlib import Path
from fastapi import status, HTTPException


def image_processing(json_image, product_category, file_extension):
    image_full_name = IMAGE_PATH + 'default_product_image.png'
    if len(json_image) > 0:
        image_dir = Path(IMAGE_PATH) / f'{str(product_category)}'
        image_dir.mkdir(parents=True, exist_ok=True)
        image_file_name = ''.join(random.choices(string.ascii_uppercase +
                                                 string.digits,
                                                 k=IMAGE_NAME_LENGTH)) + f'.{file_extension}'
        image_full_name = image_dir / image_file_name
        try:
            with open(image_full_name, 'wb+') as f:
                f.write(base64.b64decode(json_image.encode('ascii')))
        except Exception as err:
            err_message = ''
            for err_item in err.args:
                err_message += err_item
            logger.error(f'Error: {str(err)} {err_message}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f'Error {str(err)} {err_message}')
    return image_full_name
