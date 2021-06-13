import argparse
import jim
import json
import socket


ADDRESS = ''
PORT = 7777
CONNECTIONS = 10

client_name = ''


def create_parser():
    parser = argparse.ArgumentParser(description='Parser')

    parser_group = parser.add_argument_group(title='Parameters')
    parser_group.add_argument('-a', '--addr', default=ADDRESS, help='IP address')
    parser_group.add_argument('-p', '--port', type=int, default=PORT, help='TCP port')

    return parser

def init_server_socket(addr, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((addr, port))
    s.listen(CONNECTIONS)
    return s

def get_data(send):
    return json.loads(send.recv(1024).decode('utf-8'))

def send_data(client, data):
    client.send(json.dumps(data).encode('utf-8'))


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()

    socket = init_server_socket(namespace.addr, namespace.port)

    serv_addr = socket.getsockname()
    print(serv_addr)
    print(f'Server started at {serv_addr[0]}:{serv_addr[1]}')

    client, address = socket.accept()
    print(f'Client connected from {address[0]}:{address[1]}')

    while True:
        data = get_data(client)

        if client_name == '':
            if data['action'] == 'presence' and data['user']['account_name'] != '':
                client_name = data['user']['account_name']
                jim.RESPONSE['response'], jim.RESPONSE['alert'] = jim.SERV_RESP[0]
                print(f'{data["time"]} - {data["user"]["account_name"]}: {data["user"]["status"]}')
            else:
                jim.RESPONSE['response'], jim.RESPONSE['alert'] = jim.SERV_RESP[1]

        if client_name != '' and data['action'] == 'msg':
            print(f'{data["time"]} - {client_name}: {data["message"]}')
            jim.RESPONSE['response'], jim.RESPONSE['alert'] = jim.SERV_RESP[0]

            if data["message"] == 'exit':
                jim.RESPONSE['response'], jim.RESPONSE['alert'] = jim.SERV_RESP[2]

        send_data(client, jim.RESPONSE)

        if jim.RESPONSE['response'] != '200':
            client.close()
            break

    socket.close()