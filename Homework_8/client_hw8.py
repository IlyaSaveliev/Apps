import sys
import jim_v2
import logging.config
import argparse
import socket
import json
import logging
from decorator import log
import select
import multiprocessing

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

def get_send(socket):
    while True:
        msg = input('Введите сообщение ("exit" для выхода): ')

        if msg:
            print(msg)
            jim_v2.MESSAGE['message'] = msg

            try:
                send_data(socket, jim_v2.MESSAGE)
            except ConnectionResetError as e:
                logger.error(e)
                break

def get_receive(socket):
    while True:
        try:
            data = get_data(socket)
        except ConnectionResetError as e:
            logger.error(e)
            break

        if data['response'] != '200':
            logger.debug('Ending')
            break

        if 'messages' in data:
            for message in data['messages']:
                sys.stdout.write(f'{message["time"]} - {message["from"]}: {message["message"]}')

def main() -> None:
    logger.info('Started')

    parser = create_parser()
    namespace = parser.parse_args()

    client_name = input('Введите имя: ')

    socket = init_client_socket(namespace.addr, namespace.port)

    send = get_send(socket)
    receive = get_receive(socket)

    serv_addr = socket.getpeername()
    client_start = f'Connected to server: {serv_addr[0]}:{serv_addr[1]}'
    print(client_start)
    logger.info(client_start)

    jim_v2.PRESENCE['user']['account_name'] = client_name
    try:
        send_data(socket, jim_v2.PRESENCE)
    except ConnectionError as e:
        logger.error(e)
        socket.close()
        exit(1)

    p_send = multiprocessing.Process(target=send, args=(socket,))
    p_receive = multiprocessing.Process(target=receive, args=(socket,))

    p_send.start()
    p_receive.start()

    if not p_send.is_alive() or not p_receive.is_alive():
        exit(1)

    p_send.join()
    p_receive.join()
    socket.close()

    # while True:
    #     r = []
    #
    #     try:
    #         r, w, e = select.select([socket], [], [], 1)
    #     except Exception as e:
    #         logger.error(e)
    #
    #     if socket in r:
    #         try:
    #             data = get_data(socket)
    #         except ConnectionResetError as e:
    #             logger.error(e)
    #             break
    #
    #         if data['response'] != '200':
    #             logger.debug('Ending')
    #             break
    #
    #         if 'messages' in data:
    #             for message in data['messages']:
    #                 print(f'{message["time"]} - {message["from"]}: {message["message"]}')
    #
    #     else:
    #         msg = input('Введите сообщение ("exit" для выхода): ')
    #         if msg:
    #             jim_v2.MESSAGE['message'] = msg
    #
    #             try:
    #                 send_data(socket, jim_v2.MESSAGE)
    #             except ConnectionResetError as e:
    #                 logger.error(e)
    #                 break
    #
    # socket.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)
