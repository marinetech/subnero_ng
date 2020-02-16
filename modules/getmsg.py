from unetpy import *
import time

class GetMsg:
    def __init__(self, sock):
        self.sock = sock


    def id(self):
        print()
        print("Task Type: GetMsg")


    def exec_step(self):
        print()
        print("-I- Wating for message")
        rx = self.sock.receive()
        print('from node', rx.from_, ':', bytearray(rx.data).decode())


if __name__ == "__main__":
    # sock = UnetSocket("192.168.0.11", 1100)
    sock = UnetSocket("localhost", 1102)
    task = GetMsg(sock)
    task.id()
    task.exec_step()
