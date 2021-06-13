import socket
import jim
import json
import argparse

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
    s.connect((addr, port))
    return s

def send_data(client, data):
    client.send(json.dumps(data).encode('utf-8'))

def get_data(send):
    return json.loads(send.recv(1024).decode('utf-8'))


if __name__ == '__main__':
    client_name = input('Username: ')

    parser = create_parser()
    namespace = parser.parse_args()

    socket = init_client_socket(namespace.addr, namespace.port)

    serv_addr = socket.getpeername()
    print(serv_addr)
    print(f'Connected to server: {serv_addr[0]}:{serv_addr[1]}')

    jim.PRESENCE['user']['account_name'] = client_name
    send_data(socket, jim.PRESENCE)

    while True:
        data = get_data(socket)

        if data['response'] != '200':
            break

        msg = input('Enter your message ("exit" to exit): ')
        jim.MESSAGE['message'] = msg
        send_data(socket, jim.MESSAGE)

    socket.close()