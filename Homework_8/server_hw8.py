import jim_v2
import logging.config
import argparse
import socket
import json
import logging
from decorator import log
import select

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('server_log')

ADDRESS = ''
PORT = 7777
CONNECTIONS = 10
TIMEOUT = 0.2




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
        s.settimeout(TIMEOUT)
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


def mainloop() -> None:
    waiting_counter = 0
    clients = []
    clients_info = {}

    logger.info('Started')

    parser = create_parser()
    namespace = parser.parse_args()

    socket = init_server_socket(namespace.addr, namespace.port)

    serv_addr = socket.getsockname()
    server_start = f'Server started: {serv_addr[0]}:{serv_addr[1]}'
    print(server_start)
    logger.info(server_start)

    while True:
        messages = []

        try:
            client, client_addr = socket.accept()
        except OSError as e:
            pass
        else:
            info = f'Client connected from {client_addr[0]}:{client_addr[1]}'
            print(info)
            logger.info(info)
            client_info = {'name': '', 'addr': client_addr, 'in_messages': []}
            clients.append(client)
            clients_info[client] = client_info
        finally:
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], 0)
            except Exception as e:
                logger.error(e)

            for s_client in r:
                try:
                    data_in = get_data(s_client)
                except ConnectionResetError as e:
                    logger.error(e)

                if clients_info[s_client]['name'] == '':
                    if data_in['action'] == 'presence' and data_in['user']['account_name'] != '':
                        clients_info[s_client]['name'] = data_in['user']['account_name']
                        jim_v2.RESPONSE['response'], jim_v2.RESPONSE['alert'] = jim_v2.SERV_RESP[0]
                        print(f'{data_in["time"]} - {data_in["user"]["account_name"]}: {data_in["user"]["status"]}')
                    else:
                        jim_v2.RESPONSE['response'], jim_v2.RESPONSE['alert'] = jim_v2.SERV_RESP[1]

                if clients_info[s_client]['name'] != '' and data_in['action'] == 'msg':
                    data_in['from'] = clients_info[s_client]["name"]
                    print(f'{data_in["time"]} - {data_in["from"]}: {data_in["message"]}')
                    jim_v2.RESPONSE['response'], jim_v2.RESPONSE['alert'] = jim_v2.SERV_RESP[0]

                    messages.append(data_in)

                    if data_in["message"] == 'exit':
                        jim_v2.RESPONSE['response'], jim_v2.RESPONSE['alert'] = jim_v2.SERV_RESP[2]

                clients_info[s_client]['data_out'] = jim_v2.RESPONSE

            for s_client in clients:
                clients_info[s_client]['in_messages'].extend(messages)

            for s_client in w:
                if 'data_out' in clients_info[s_client]:
                    data_out = clients_info[s_client]['data_out']
                    data_out['messages'] = clients_info[s_client]['in_messages']

                    try:
                        send_data(s_client, data_out)
                        clients_info[s_client].pop('data_out')
                        clients_info[s_client]['in_messages'].clear()
                    except ConnectionResetError as e:
                        logger.error(e)
                        clients.remove(s_client)
                        clients_info.pop(s_client)

                    if data_out['response'] != '200':
                        clients.remove(s_client)
                        clients_info.pop(s_client)

        if len(clients) == 0:
            waiting_counter += 1

        if waiting_counter > 1000:
            break

    socket.close()

    logger.debug('Socket close. Ending')


if __name__ == '__main__':
    try:
        mainloop()
    except Exception as error:
        print(error)