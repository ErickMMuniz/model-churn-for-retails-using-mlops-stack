import logging
from functools import wraps
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ROOT_PROJECT_PATH_FOR_NOTEBOOKS: str = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

def log_function_call(func):
    @wraps(func)  
    def wrapper(*args, **kwargs):
        logger.info(f"Calling function '{func.__name__}', kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Function '{func.__name__}' returned with success")
            return result
        except Exception as e:
            logger.error(f"Function '{func.__name__}' raised an exception: {e}", exc_info=True)
            raise  
    return wrapper
