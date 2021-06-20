from functools import wraps
import inspect
import logging.config

logging.config.fileConfig('logging.ini')
server_logger = logging.getLogger('server_log')
client_logger = logging.getLogger('client_log')

def log(func):
    @wraps(func)
    def call(*args, **kwargs):
        outer_func = inspect.stack()[1][3]
        server_logger.debug(f'Function {func.__name__} is called into {outer_func}')
        client_logger.debug(f'Function {func.__name__} is called into {outer_func}')
        return func(*args, **kwargs)
    return call