import bluetooth


class BtInterface():  # Interface that provides server code for RFCOMM sockets
    def __init__(self):
        self.BT_PORT = 4
        self.server_sock = None
        self.client_sock = None
        self.connected_to_bt = False

    # Using Service Discovery Protocol (SDP)
    def init_bt_conn(self):
        try:
            self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.server_sock.bind(("",self.BT_PORT))
            self.server_sock.listen(1)

            uuid = "00001101-0000-1000-8000-00805F9B34FB"

            bluetooth.advertise_service(self.server_sock,
                                        "MDPGrp2BT",
                                        uuid,
                                        service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
                                        profiles = [ bluetooth.SERIAL_PORT_PROFILE ]
                                        )

            print("[BT]Waiting for connection on RFCOMM channel %d" % self.BT_PORT)

            self.client_sock, client_addr = self.server_sock.accept()
            print("[BT]Accepted connection from: ", client_addr)
            self.connected_to_bt = True

        except Exception as e:
            print("\n[BT]Error: %s" % str(e))

    def write(self, message):
        self.client_sock.send(message)

    def read(self):
        bt_message = self.client_sock.recv(1024)  # is a buffervalue needed?
        return bt_message

    def close_socket(self):
        if self.client_sock:
            self.client_sock.close()
            print("[BT]Closing Client Socket")
        if self.server_sock:
            self.server_sock.close()
            print("[BT]Closing Server Socket")
        self.connected_to_bt = False

    def get_bt_status(self):
        return self.connected_to_bt

# Code for testing
if __name__ == "__main__":
    print("Testing bt connection")
    bt = BtInterface()
    bt.init_bt_conn()

    while True:
       	if bt.get_bt_status():
        	print("data received from laptop: %s" % bt.read())
	else:
		continue
    print("Closing Sockets")
    pc.close_socket()
