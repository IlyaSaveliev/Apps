import logging
from logging.handlers import TimedRotatingFileHandler
import locale


encoding = locale.getpreferredencoding()
formatter = logging.Formatter("%(asctime)s - %(levelname)-10s - %(module)s - %(message)s ")


log_handler = TimedRotatingFileHandler('server.log', when='D', backupCount=5, encoding=encoding)

log_handler.setFormatter(formatter)

logger = logging.getLogger('server_log')
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

def main() -> None:
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.info('Test')



if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)
