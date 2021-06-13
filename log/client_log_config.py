import logging
from logging.handlers import TimedRotatingFileHandler
import locale


encoding = locale.getpreferredencoding()
formatter = logging.Formatter("%(asctime)s - %(levelname)-10s - %(module)s - %(message)s ")


log_handler = TimedRotatingFileHandler('client.log', when='D', backupCount=5, encoding=encoding)

log_handler.setFormatter(formatter)

logger = logging.getLogger('client_log')
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

def main() -> None:
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.info('Test client.log')



if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)
