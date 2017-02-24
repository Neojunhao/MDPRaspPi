from threading import Thread
from queue import Queue
import time
from pc_api import *
from bt_api import *
from serial_api import *
from threading import Lock

print_lock = Lock()

# Initialise queues for respective connections
serial_q = Queue(10)
pc_q = Queue(10)
bt_q = Queue(10)

# Setting a arbitrary delay for each read write function
delay = 0.5


class Main(Thread):
    def __init__(self):

        self.serial_thread = SerialInterface()
        self.pc_thread = PcInterface()
        self.bt_thread = BtInterface()

        # Initialise respective connections
        self.serial_thread.init_sr_conn()
        self.pc_thread.init_pc_conn()
        self.bt_thread.init_bt_conn()

    # The following are the read write functions for each connection

    def read_pc(self):
        while 1:
            pc_message = self.pc_thread.read()
            if pc_message != '':
                bt_q.append(pc_message)
                serial_q.append(pc_message)
                print("Read from PC: %s" % (time.ctime(),pc_message))
            time.sleep(delay)

    def write_pc(self):
        while 1:
            time.sleep(delay)
            if len(pc_q)>0:
                message = pc_q.popleft()
                self.pc_thread.write(message)
                print("Wrote to PC: %s" % time.ctime(), message)

    def read_bt(self):
        while 1:
            bt_message = self.bt_thread.read()
            if bt_message != '':
                pc_q.append(bt_message)
                serial_q.append(bt_message)
                print("Read from Bt: %s" % (time.ctime(),bt_message))
            time.sleep(delay)

    def write_bt(self):
        while 1:
            time.sleep(delay)
            if len(bt_q) > 0:
                message = bt_q.popleft()
                self.bt_thread.write(message)
                print("Wrote to Bt: %s" % time.ctime(), message)

    def read_serial(self):
        while 1:
            serial_message = self.bt_thread.read()
            if serial_message != '':
                bt_q.append(serial_message)
                serial_q.append(serial_message)
                print("Read from Serial: %s" % (time.ctime(),serial_message))
            time.sleep(delay)

    def write_serial(self):
        while 1:
            time.sleep(delay)
            if len(serial_q) > 0:
                message = serial_q.popleft()
                self.serial_thread.write(message)
                print("Wrote to PC: %s" % time.ctime(), message)

    def init_threads(self):
        serial_write_thread = Thread(target=self.write_serial, name="serial_write_thread")
        serial_read_thread = Thread(target=self.read_serial, name="serial_read_thread")
        pc_write_thread = Thread(target=self.write_pc, name="pc_write_thread")
        pc_read_thread = Thread(target=self.read_pc, name="pc_read_thread")
        bt_write_thread = Thread(target=self.write_bt, name="bt_write_thread")
        bt_read_thread = Thread(target=self.read_bt, name="bt_read_thread")

        # Classify all threads as daemon (Threads die when main thread die)
        serial_write_thread.daemon = True
        serial_read_thread.daemon = True
        pc_write_thread.daemon = True
        pc_read_thread.daemon = True
        bt_write_thread.daemon = True
        bt_read_thread.daemon = True

        # Start all threads
        serial_read_thread.start()
        pc_write_thread.start()
        pc_read_thread.start()
        bt_write_thread.start()
        bt_read_thread.start()

        print("Initialised all threads")

    def close_all_sockets(self):
        self.serial_thread.close_socket()
        self.pc_thread.close_socket()
        self.bt_thread.close_socket()
        print("Closed all sockets")

if __name__ == "__main__":
    main = Main()
    main.init_threads()
    # Keep main thread alive
    while True:
        time.sleep(1)
    main.close_all_sockets()