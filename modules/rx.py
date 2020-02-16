from unetpy import *
import time
import os
import numpy as np

class Rx:
    def __init__(self, sock, number_of_recs, rec_size, rx_out_folder, rx_out_file, sleep_between_loops):
        self.sock = sock
        self.number_of_recs = number_of_recs
        self.rec_size = rec_size
        self.rx_out_folder = rx_out_folder
        self.rx_out_file = rx_out_file
        self.sleep_between_loops = str(sleep_between_loops)

        # If necessary, create out folder
        i = 1
        folder_to_create = rx_out_folder
        while os.path.exists(folder_to_create):
            folder_to_create = rx_out_folder + "_" + str(i)
            i = i + 1
        os.makedirs(folder_to_create)


    def id(self):
        print()
        print("Task Type: Rx")
        print("number_of_recs: " + str(self.number_of_recs))
        print("rec_size: " + str(self.rec_size))
        print("rx_out_folder: " + str(self.rx_out_folder))
        print("rx_out_file: " + str(self.rx_out_file))
        print("sleep_between_loops: " + str(self.sleep_between_loops))


    def exec_step(self):
        gw = self.sock.getGateway()
        bb = gw.agentForService(Services.BASEBAND) # lookup the agent providing baseband service

        file_idx = 0
        for i in range(0, self.number_of_recs):
            print("-I- rx #" + str(i+1))
            bb << RecordBasebandSignalReq(recLen=self.rec_size) # Record a baseband signal
            rxntf = gw.receive(RxBasebandSignalNtf, timeout=5000)
            if rxntf is not None:
                # what is the next avaiable file name?
                next_out_file = "{}/{}{}".format(self.rx_out_folder, self.rx_out_file, file_idx)
                file_idx = file_idx + 1
                # Extract the recorded signal
                rec_signal = rxntf.signal
                # rec_signal.tofile(next_out_file)
                np.savetxt(next_out_file, rec_signal)
                print('-I- signal was recorded successfully')
            else:
                print('-E- signal was not recorded successfully')


if __name__ == "__main__":
    # sock = UnetSocket("192.168.0.11", 1100)
    sock = UnetSocket("localhost", 1101)
    task = Rx(sock, 1, 192000, "/home/ilan/projects/subnero_ng/out/test", "test", 0)
    task.id()
    # task.exec_step()
    sock.close()
