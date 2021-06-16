import jim_v2
import logging.config
import argparse
import socket
import json
import logging
import inspect
from functools import wraps
import log.server_log_config

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('client_log')

ADDRESS = '127.0.0.1'
PORT = 7777

def log(func):
    @wraps(func)
    def call(*args, **kwargs):
        outer_func = inspect.stack()[1][3]
        logger.debug(f'Function {func.__name__} is called into {outer_func}')
        return func(*args, **kwargs)
    return call

def create_parser():
    parser = argparse.ArgumentParser(description='Parser')

    parser_group = parser.add_argument_group(title='Parameters')
    parser_group.add_argument('-a', '--addr', default=ADDRESS, help='IP address')
    parser_group.add_argument('-p', '--port', type=int, default=PORT, help='TCP port')

    return parser

@log
def init_client_socket(addr, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((addr, port))
    except Exception as error:
        logger.error(f'Client socket error: {error}')
    else:
        logger.info('Client socket OK!')
        return s

@log
def send_data(client, data):
    try:
        client.send(json.dumps(data).encode('utf-8'))
    except Exception as error:
        logger.error(f'Send_data error: {error}')

@log
def get_data(send):
    try:
        return json.loads(send.recv(1024).decode('utf-8'))
        # return pickle.loads(data)
    except Exception as error:
        logger.error(f'Get_data error: {error}')

def main() -> None:
    client_name = input('Username: ')
    logger.info(f'Connetion user: {client_name}')

    parser = create_parser()
    namespace = parser.parse_args()

    socket = init_client_socket(namespace.addr, namespace.port)

    serv_addr = socket.getpeername()
    print(serv_addr)
    print(f'Connected to server: {serv_addr[0]}:{serv_addr[1]}')

    jim_v2.PRESENCE['user']['account_name'] = client_name
    send_data(socket, jim_v2.PRESENCE)

    while True:
        data = get_data(socket)

        if data['response'] != '200':
            break

        msg = input('Enter your message ("exit" to exit): ')
        jim_v2.MESSAGE['message'] = msg
        send_data(socket, jim_v2.MESSAGE)
        logger.info('Socket close')

    socket.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)
