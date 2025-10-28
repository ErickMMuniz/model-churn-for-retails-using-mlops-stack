import logging
from functools import wraps

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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


def from_str_to_type(type_name: str):
    match type_name:
        case 'int':
            return int
        case 'float':
            return float
        case 'str':
            return str
        case 'bool':
            return bool
        case 'datetime':
            return 'datetime64[ns]'
        case _:
            return 'object'