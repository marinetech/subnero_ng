import sys
import os
import time
import numpy as np
import arlpy as ap
from unetpy import *


class TxRx:
    def __init__(self, sock, signal_file, power_level, number_of_loops, sleep_between_loops, fc, rec_size, rx_out_folder, rx_out_file):
        self.sock = sock
        self.signal_file = signal_file
        self.power_level = power_level
        self.number_of_loops = number_of_loops
        self.sleep_between_loops = sleep_between_loops
        self.fc = fc
        self.rec_size = rec_size
        self.rx_out_folder = rx_out_folder
        self.rx_out_file = rx_out_file

        i = 1 # create out folder
        folder_to_create = rx_out_folder
        while os.path.exists(folder_to_create):
                folder_to_create = rx_out_folder + "_" + str(i)
                i = i + 1
        os.makedirs(folder_to_create)

        try:
            self.signal = np.loadtxt(signal_file)
        except Exception as ex:
            print(str(ex))
            print("-E- failed to load signal file")
            exit(1)

    def id(self):
        print()
        print("Task Type: TxRx")
        print("Signal: " + self.signal_file)
        print("Power_level: " + str(self.power_level))
        print("Number_of_loops: " + str(self.number_of_loops))
        print("Sleep_between_loops: " + str(self.sleep_between_loops))
        print("fc: " + str(self.fc))
        print("rec_size: " + str(self.rec_size))
        print("rx_out_folder: " + self.rx_out_folder)
        print("rx_out_file: " + self.rx_out_file)
        print()

    def exec_step(self):
        gw = self.sock.getGateway()
        bb = gw.agentForService(Services.BASEBAND)

        file_idx = 0
        for i in range(0,self.number_of_loops):
            print("-I- Tx #" + str(i+1) + " " + self.signal_file)
            bb << TxBasebandSignalReq(signal=self.signal.tolist(), fc=self.fc, fs=self.rec_size)
            gw.flush()

            print("-I- rx #" + str(i+1))
            # Record a baseband signal
            bb << RecordBasebandSignalReq(recLen=self.rec_size)

            rxntf = gw.receive(RxBasebandSignalNtf, timeout=5000)
            if rxntf is not None:
                # what is the next avaiable file name?
                next_out_file = "{}/{}{}".format(self.rx_out_folder, self.rx_out_file, file_idx)
                file_idx = file_idx + 1

                # Extract the recorded signal
                rec_signal = rxntf.signal
                # rec_signal.tofile(next_out_file)
                np.savetxt(next_out_file, rec_signal)
                print("-I- signal was recorded successfully\n")
            else:
                print("-E- signal was not recorded successfully\n")


if __name__ == "__main__":
    # sock = UnetSocket("192.168.0.11", 1100)
    sock = UnetSocket("localhost", 1101)
    task = TxRx(sock, "/home/ilan/projects/subnero_ng/signals/subnero.sig", -120, 2, 2, 0,192000, "/home/ilan/projects/subnero_ng/out/txrx", "txrx_test_" )
    task.id()
    task.exec_step()
