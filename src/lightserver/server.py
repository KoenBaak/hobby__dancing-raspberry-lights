from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(1)
        self.active_client = None
        self.chunk_size = None
        self.rate = None
        self.channels = None

    def client_data_generator(self):
        while True:

            # read msg
            data = b''
            n = 0
            while n < self.chunk_size:
                packet = self.active_client.recv(self.chunk_size - n)
                if not packet:
                    break
                data += packet
                n = len(data)

            if len(data) < self.chunk_size:
                break

            yield data

    def handshake(self):
        data = b''
        while data.decode('utf-8').count(';') < 3:
            packet = self.active_client.recv(100)
            if not packet:
                return False
            data += packet

        self.chunk_size, self.rate, self.channels = list(map(int, data.decode('utf-8').split(';')[:3]))
        self.active_client.sendall(b"ACCEPT;")
        return True

    def run(self, strip_manager):
        while True:
            self.active_client, _ = self.sock.accept()

            if not self.handshake():
                self.close_client_connection()
                continue

            stream = self.client_data_generator()

            # visualize audio until connection is broken
            strip_manager.visualize_audio(stream, self.chunk_size, self.rate, self.channels)

            # close connection on this side
            self.close_client_connection()

    def close_client_connection(self):
        print("clossing connection")
        self.active_client.close()
        self.active_client = None
        self.channels = None
        self.chunk_size = None
        self.rate = None

    def shutdown(self):
        if self.active_client is not None:
            self.active_client.close()
        self.sock.close()
