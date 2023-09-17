from socket import socket, AF_INET, SOCK_STREAM


class Client:
    def __init__(self, host, port):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.host = host
        self.port = port

    def close(self):
        self.sock.close()

    def handshake(self, chunk_size, rate, channels):
        initial_message = f"{chunk_size};{rate};{channels};"
        self.sock.sendall(initial_message.encode("utf-8"))

        response = b""
        while ";" not in response.decode("utf-8"):
            packet = self.sock.recv(100)
            if not packet:
                return False
            response += packet

        return response.decode("utf-8") == "ACCEPT;"

    def run(self, stream, chunk_size, rate, channels):
        self.sock.connect((self.host, self.port))

        accepted = self.handshake(chunk_size, rate, channels)

        if not accepted:
            print("Connection is not accepted")
            return

        print("starting")
        while True:
            data = stream.read(chunk_size)
            sent = self.sock.sendall(data)
