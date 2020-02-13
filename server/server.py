from socket import socket, AF_INET, SOCK_STREAM
from time import sleep
import sys, os
sys.path.append(os.path.join(os.getcwd(), 'logger'))
from logger.log import logger_decorator


class ServerListener:
    @logger_decorator('info')
    def __init__(self, port: int, allowed: str = '', listen_timeout: int = 5):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.allowed = allowed
        self.port = port
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
    MS = ServerListener(8888)
    MS.start_listen()
    MS.answer_connections()
