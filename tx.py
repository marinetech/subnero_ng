import env
from task import *

class Tx(Task):
    def __init__(self, ip_address, signal,  number_of_loops=1, sleep_between_loops=0):
        super().__init__(ip_address)
        self.siganl = signal
        self.number_of_loops = number_of_loops
        self.sleep_between_loops = sleep_between_loops


    def exec(self):
        bb = modem.agentForService(Services.BASEBAND)
        for i in range(0, self.number_of_loops):
            print("-I- Tx #" + str(i+1) + " " + self.siganl)
            bb << org_arl_unet_bb.TxBasebandSignalReq(signal=signal.tolist(), fc=0, fs=192000)
            txntf4 = modem.receive(TxFrameNtf, 5000)
            if txntf4 is not None:
                # Request a recording from txTime onwards
                bb << RecordBasebandSignalReq(recTime=txntf4.txTime, recLen=(len(tx_signal)*2))
            else:
                print('Transmission not successfull, try again!')

            if self.sleep_between_loops:
                print("-I- sleeping for {} seconds".format(sleep_between_loops))
                time.sleep(sleep_between_loops)
