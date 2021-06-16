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
logger = logging.getLogger('server_log')

ADDRESS = ''
PORT = 7777
CONNECTIONS = 10

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
def init_server_socket(addr, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((addr, port))
    try:
        s.listen(CONNECTIONS)
    except Exception as error:
        logger.error(f'Server socket error: {error}')
    else:
        logger.info('Socket_init OK')
        return s
@log
def get_data(send):
    try:
        return json.loads(send.recv(1024).decode('utf-8'))
        # return pickle.loads(data)
    except Exception as error:
        logger.error(f'Get_data error: {error}')

@log
def send_data(client, data):
    try:
        client.send(json.dumps(data).encode('utf-8'))
    except Exception as error:
        logger.error(f'Send_data error: {error}')


def main() -> None:
    parser = create_parser()
    namespace = parser.parse_args()
    client_name = ''

    socket = init_server_socket(namespace.addr, namespace.port)

    serv_addr = socket.getsockname()
    print(f'Server started at {serv_addr[0]}:{serv_addr[1]}')
    logger.info('Start')

    client, address = socket.accept()
    print(f'Client connected from {address[0]}:{address[1]}')

    while True:
        data = get_data(client)

        if client_name == '':
            if data['action'] == 'presence' and data['user']['account_name'] != '':
                client_name = data['user']['account_name']
                jim_v2.RESPONSE['response'], jim_v2.RESPONSE['alert'] = jim_v2.SERV_RESP[0]
                print(f'{data["time"]} - {data["user"]["account_name"]}: {data["user"]["status"]}')
            else:
                jim_v2.RESPONSE['response'], jim_v2.RESPONSE['alert'] = jim_v2.SERV_RESP[1]

        if client_name != '' and data['action'] == 'msg':
            print(f'{data["time"]} - {client_name}: {data["message"]}')
            jim_v2.RESPONSE['response'], jim_v2.RESPONSE['alert'] = jim_v2.SERV_RESP[0]

            if data["message"] == 'exit':
                jim_v2.RESPONSE['response'], jim_v2.RESPONSE['alert'] = jim_v2.SERV_RESP[2]

        send_data(client, jim_v2.RESPONSE)

        if jim_v2.RESPONSE['response'] != '200':
            client.close()
            break

    socket.close()
    logger.info('Socket close')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)