from unetpy import *
import time

class SendMsg:
    def __init__(self, sock, recipient, power_level, txt, number_of_loops=1, sleep_between_loops=0):
        self.sock = sock
        self.recipient = recipient
        self.power_level = power_level
        self.number_of_loops = number_of_loops
        self.sleep_between_loops = sleep_between_loops
        self.txt = txt


    def id(self):
        print()
        print("Task Type: SendMsg")
        print("Text: " + self.txt)
        print("Recipient: " + str(self.recipient))
        print("Power_level: " + str(self.power_level))
        print("Number_of_loops: " + str(self.number_of_loops))
        print("Sleep_between_loops: " + str(self.sleep_between_loops))


    def exec_step(self):
        for count in range(self.number_of_loops):
            print()
            print("-I- Sending string #" + str(count+1))
            self.sock.send(self.txt, self.recipient)
            if self.sleep_between_loops:
                print("-I- sleeping for {} seconds".format(sleep_between_loops))
                time.sleep(self.sleep_between_loops)


if __name__ == "__main__":
    # sock = UnetSocket("192.168.0.11", 1100)
    sock = UnetSocket("localhost", 1101)
    task = SendMsg(sock, 31, -120, "hello", 1, 0)
    task.id()
    task.exec_step()
