modem = '192.168.0.11'
power_level = -40 #Max:0; Min:-138
signal_file = '../signals/subnero.sig'
rec_size = 192000
rx_out_folder = "out/rx_out"
rx_out_file = "rx_rec_"
sleep_between_loops = 2 #seconds
number_of_loops = 3


#----------------------------------------#
import sys
import os
import time
import numpy as np
import arlpy as ap
from unetpy import *

# Open connection to the modem
print("-I- connecting to modem: " + modem)
try:
    sock = UnetSocket(modem, 1100)
    gw = sock.getGateway()
except:
    exit(1)

# If necessary, create out folder
i = 1
folder_to_create = rx_out_folder
while os.path.exists(folder_to_create):
        folder_to_create = rx_out_folder + "_" + str(i)
        i = i + 1
os.makedirs(folder_to_create)


print("-I- loading signal from: " + signal_file)
try:
    signal = np.loadtxt(signal_file)
except Exception as ex:
    print(str(ex))
    print("-E- failed to load signal file")
    exit(1)


#----------------------------------------#
# lookup the agent providing baseband service
bb = gw.agentForService(Services.BASEBAND)

file_idx = 0
for i in range(0,number_of_loops):
    print("-I- Tx #" + str(i+1) + " " + signal_file)
    bb << TxBasebandSignalReq(signal=signal.tolist(), fc=0, fs=192000)

    gw.flush()

    print("-I- rx #" + str(i+1))
    # Record a baseband signal
    bb << RecordBasebandSignalReq(recLen=rec_size)

    rxntf = gw.receive(RxBasebandSignalNtf, timeout=5000)
    if rxntf is not None:
        # what is the next avaiable file name?
        next_out_file = "{}/{}{}".format(rx_out_folder, rx_out_file, file_idx)
        file_idx = file_idx + 1

        # Extract the recorded signal
        rec_signal = rxntf.signal
        # rec_signal.tofile(next_out_file)
        np.savetxt(next_out_file, rec_signal)
        print('-I- signal was recorded successfully')
    else:
        print('-E- signal was not recorded successfully')




sock.close()
