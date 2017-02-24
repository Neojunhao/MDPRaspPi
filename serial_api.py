import serial
import time


class SerialInterface():
    def __init__(self):
        self.usb_interface = "/dev/ttyACM0"  # interface file that is automatically created on connection
        self.baud_rate = 9600
        self.ser = None
        self.connected_to_sr = False

    def init_sr_conn(self):
        try:
            self.ser = serial.Serial(self.usb_interface,self.baud_rate)
            self.connected_to_sr = True
            print("[SR]Connected via Serial")
        except Exception as e:
            print("\n[SR]Error: %s" % str(e))

    def write(self, message):
        try:
            self.ser.write(message)
        except Exception as e:
            print("\n[SR]Error on Serial Write: %s" % str(e))
            self.close_socket()
            time.sleep(2)
            self.init_sr_conn()

    def read(self):
        try:
            sr_message = self.ser.readline()
            print("[SR]Received message from Arduino: %s" % sr_message)
            return sr_message
        except Exception as e:
            print("\n[SR]Error on Serial WRead: %s" % str(e))
            self.close_socket()
            time.sleep(2)
            self.init_sr_conn()

    def close_socket(self):
        if self.ser:
            self.ser.close()
            self.connected_to_sr = False
            print("[SR]Serial Socket Closed")

    def get_sr_status(self):
        return self.connected_to_sr

if __name__ == "__main__":
    print("Testing Serial Connection")
    sr = SerialInterface()
    sr.init_sr_conn()

    while True:
        # message = input()
        message = b"A"
        print("Writing [%s] to arduino" % message)
        sr.write(message)

        # code to run at arduino
        # Serial.begin(9600)
        # Serial.println("text here")
        print("read")
        print("data received [%s] from arduino" % sr.read().translate(None,b'\r\n').decode("ascii"))

    print("Closing Sockets")
    sr.close_socket()
