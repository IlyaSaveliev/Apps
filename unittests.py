import unittest
import server
import client
import socket
import warnings

class TestServer(unittest.TestCase):

    def setUp(self):
        self.s = server.init_server_socket('0.0.0.0', 7777)

    def test_socket_is_socket(self):
        self.assertIsInstance(self.s, socket.socket)

    def test_server_socket_addr(self):
        self.assertEqual(self.s.getsockname(), ('0.0.0.0', 7777))

    def tearDown(self):
        self.s.close()

class TestClient(unittest.TestCase):

    def setUp(self):
        self.s = server.init_server_socket('0.0.0.0', 7777)
        self.c = client.init_client_socket('127.0.0.1', 7777)
        self.send = self.s.accept()[0]
        client.send_data(self.c, {'unittest': 'unittest'})
        warnings.simplefilter("ignore", ResourceWarning)

    def test_get_data(self):
        self.assertEqual(client.get_data(self.send), {'unittest': 'unittest'})

    def test_send_data(self):
        with self.assertRaises(TypeError):
            client.send_data()

    def tearDown(self):
        self.c.close()
        self.s.close()


if __name__ == '__main__':
    unittest.main()
