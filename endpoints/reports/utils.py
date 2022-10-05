from app_logger import logger
import base64


def doc_to_base64(file_name: str):
    encoded_string = ''
    try:
        with open(file_name, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('ascii')
    except Exception as err:
        logger.error(f'For file:"{file_name}" error "{str(err)}" occured!!!')
    finally:
        return encoded_string
