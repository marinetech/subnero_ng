from unetpy import *
from arlpy import *
import numpy as np
import time

class Tx:
    def __init__(self, sock, signal_file, power_level, number_of_loops=1, sleep_between_loops=0, fc=0):
        self.sock = sock
        self.signal_file = signal_file
        self.power_level = power_level
        self.number_of_loops = number_of_loops
        self.sleep_between_loops = sleep_between_loops
        self.fc = fc
        try:
            self.signal = np.loadtxt(signal_file)
        except Exception as ex:
            print("-E- failed to load signal file")
            print(str(ex))
            exit()


    def id(self):
        print()
        print("Task Type: Tx")
        print("Signal: " + self.signal_file)
        print("Power_level: " + str(self.power_level))
        print("Number_of_loops: " + str(self.number_of_loops))
        print("Sleep_between_loops: " + str(self.sleep_between_loops))
        print("fc: " + str(self.fc))


    def exec_step(self):
        print()
        gw = self.sock.getGateway()
        bb = gw.agentForService(Services.BASEBAND)
        for i in range(0, self.number_of_loops):
            print("-I- Tx #" + str(i+1) + " " + self.signal_file)
            bb << TxBasebandSignalReq(signal=self.signal.tolist(), fc=self.fc, fs=192000)
            txntf4 = gw.receive(TxFrameNtf, 5000)
            if txntf4 is None:
                print('-E- transmission was not successfull')
            if self.sleep_between_loops:
                print("-I- sleeping for {} seconds".format(self.sleep_between_loops))
                time.sleep(self.sleep_between_loops)


if __name__ == "__main__":
    # sock = UnetSocket("192.168.0.11", 1100)
    sock = UnetSocket("localhost", 1101)
    task = Tx(sock, "/home/ilan/projects/subnero_ng/signals/subnero.sig", -120, 2, 2, 0)
    task.id()
    # task.exec_step()
