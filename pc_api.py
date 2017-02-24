import socket
# import time
# import sys


class PcInterface():

    def __init__(self):
        self.TCP_IP = "192.168.2.1"
        self.TCP_PORT = 8080
        self.conn = None
        self.client = None
        self.addr = None
        self.connected_to_pc = False

    # function creates a TCP/IP socket
    def init_pc_conn(self):
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Allow reuse of port/IP
            self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.conn.bind((self.TCP_IP, self.TCP_PORT))
            self.conn.listen(1)
            print("[PC]Listening for incoming connections...")
            self.client, self.addr = self.conn.accept()
            print("[PC]Connected to:", self.addr)
            self.connected_to_pc = True
        except Exception as e:
            print("\n[PC]Error: %s" % str(e))

    def write(self, message):
        try:
            self.client.sendto(message, self.addr)
            print("[PC]sent message: %s" % message)
        except Exception as e:
            print("\n[PC]Write error: %s" % str(e))
            self.close_socket()
            self.init_pc_conn()

    def read(self):
        try:
            pc_message = self.client.recv(1024)  # recv(buffersize)?
            print("[PC]Read message: %s" % pc_message)
            return pc_message
        except Exception as e:
            print("n\[PC] Read Error: %s" % str(e))
            self.close_socket()
            self.init_pc_conn()

    # function to close both server and client sockets
    def close_socket(self):
        if self.conn:
            self.conn.close()
            print("[PC]Closing Server Socket.")
        if self.client:
            self.client.close()
            print("[PC]Closing Client Socket")
        self.connected_to_pc = False

    # returns true if PC is connected
    def get_pc_status(self):
        return self.connected_to_pc

# Code for testing
if __name__ == "__main__":
    print("Testing wifi connection")
    pc = PcInterface()
    pc.init_pc_conn()

    while True:
        print("reading")
        print("data received from laptop: %s" % pc.read().decode())

    print("Closing Sockets")
    pc.close_socket()
