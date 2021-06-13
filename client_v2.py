import socket
import jim_v2
import json
import argparse
import pickle
import logging.config

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('client_log')

ADDRESS = '127.0.0.1'
PORT = 7777


def create_parser():
    parser = argparse.ArgumentParser(description='Parser')

    parser_group = parser.add_argument_group(title='Parameters')
    parser_group.add_argument('-a', '--addr', default=ADDRESS, help='IP address')
    parser_group.add_argument('-p', '--port', type=int, default=PORT, help='TCP port')

    return parser

def init_client_socket(addr, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((addr, port))
    except Exception as error:
        logger.error(f'Client socket error: {error}')
    else:
        logger.info('Client socket OK!')
        return s

def send_data(client, data):
    try:
        client.send(json.dumps(data).encode('utf-8'))
    except Exception as error:
        logger.error(f'Send_data error: {error}')

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
