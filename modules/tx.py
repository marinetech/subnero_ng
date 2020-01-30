from unetpy import *
from arlpy import *
import numpy as np
import time

class Tx:
    def __init__(self, sock, signal, power_level, number_of_loops=1, sleep_between_loops=0):
        self.sock = sock      
        self.signal = signal
        self.power_level = power_level
        self.number_of_loops = number_of_loops
        self.sleep_between_loops = sleep_between_loops
    

    def id(self):
        print("\n")
        print("Task Type: TX")
        print("Sock: " + self.sock)
        print("Signal: " + self.signal)
        print("Power_level: " + str(self.power_level))
        print("Number_of_loops: " + str(self.number_of_loops))
        print("Sleep_between_loops: " + str(self.sleep_between_loops))


    def exec_step(self):
        bb = sock.agentForService(Services.BASEBAND)
        for i in range(0, self.number_of_loops):
            print("-I- Tx #" + str(i+1) + " " + self.siganl)
            bb << org_arl_unet_bb.TxBasebandSignalReq(signal=signal.tolist(), fc=0, fs=192000)
            txntf4 = sock.receive(TxFrameNtf, 5000)
            if txntf4 is not None:
                # Request a recording from txTime onwards
                bb << RecordBasebandSignalReq(recTime=txntf4.txTime, recLen=(len(tx_signal)*2))
            else:
                print('Transmission not successfull, try again!')

            if self.sleep_between_loops:
                print("-I- sleeping for {} seconds".format(sleep_between_loops))
                time.sleep(sleep_between_loops)


if __name__ == "__main__":
    task = Tx("192.168.0.11", "../signals/subnero.sig", -120, 2, 2)
    task.id()
    task.exec_step()
