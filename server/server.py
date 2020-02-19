from socket import socket, AF_INET, SOCK_STREAM
from time import sleep
import sys
import os
from config import DEFAULT_PORT
sys.path.append(os.path.join(os.getcwd(), 'logger'))
from logger.log import logger_decorator


class Port:
    def __init__(self, init_value=None, name='port_number'):
        if not 1023 < init_value < 65536:
            self.wrong_port(init_value)
            exit()
        self.value = init_value
        self.name = name

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            self.wrong_port(value)
            exit()
        instance.__dict__[self.name] = value

    @logger_decorator('critical')
    def wrong_port(self, port):
        print(f'Wrong port {port}')


class ServerListener:
    port: Port(DEFAULT_PORT)
    @logger_decorator('info')
    def __init__(self, allowed: str = '', listen_timeout: int = 5):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.allowed = allowed
        self.listen_time = listen_timeout
        self.active = []

    @logger_decorator('info')
    def start_listen(self):
        self.socket.bind((self.allowed, self.port))
        self.socket.listen(self.listen_time)

    @logger_decorator('critical')
    def stop_server(self):
        self.active.clear()
        self.socket.close()

    @logger_decorator('info')
    def answer_connections(self):
        try:
            while True:
                client, address = self.socket.accept()
                client.send(f'your address is {address}\n'.encode('utf-8'))
                for i in range(self.listen_time, 0, -1):
                    client.send(f'time for connection {i}\n'.encode('utf-8'))
                    sleep(1)
                client.close()
        except KeyboardInterrupt:
            self.stop_server()


if __name__ == '__main__':
    MS = ServerListener()
    MS.start_listen()
    MS.answer_connections()
