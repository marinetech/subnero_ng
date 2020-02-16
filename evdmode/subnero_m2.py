modem = '192.168.0.11'
port = 1100
power_level = -40 #Max:0; Min:-138
signal_file = '../signals/subnero.sig'
number_of_loops = 3
sleep_between_loops = 2 #seconds
passband = 1 #0 means baseband

#---------------------------------------#
from unetpy import *
from arlpy import *
import numpy as np
import time

print("-I- connecting to modem: " + modem)
try:
    sock = UnetSocket(modem, port)
    gw = sock.getGateway()
except:
    print("-E- Failed")
    exit()

print("-I- loading signal from: " + signal_file)
try:
    signal = np.loadtxt(signal_file)
except Exception as ex:
    print(str(ex))
    print("-E- failed to load signal file")
    exit(1)

# lookup the agent providing baseband service
bb = gw.agentForService(Services.BASEBAND)
for i in range(0, number_of_loops):
    print("-I- Tx #" + str(i+1) + " " + signal_file)
    bb << TxBasebandSignalReq(signal=signal.tolist(), fc=0, fs=192000)
    txntf = gw.receive(TxFrameNtf, 5000)
    if txntf is None:
        print('-E- transmission not successfull')
    if sleep_between_loops:
        print("-I- sleeping for {} seconds".format(sleep_between_loops))
        time.sleep(sleep_between_loops)


sock.close()
