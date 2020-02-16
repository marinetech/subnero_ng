import json
import sys
from modules.tx import *
from modules.rx import *
from modules.txrx import *
from modules.sendmsg import *
from modules.getmsg import *


def usage():
    print("Usage:")
    print("\t{} path_to_json".format(sys.argv[0]))


def check_args():
    # we excpect a single command-line argument - path to json
    if len(sys.argv) < 2:
        print("-E- missing json argument")
        usage()
        exit()


def load_mission():
    global mission_steps; mission_steps = []
    global sock

    with open(sys.argv[1]) as json_file:
        mission = json.load(json_file)
        modem = mission["modem"]
        port = mission["port"]
        sock = UnetSocket(modem, port)
        for step in mission["steps"]:
            stepObj = create_task(step)
            if stepObj:
                mission_steps.append(stepObj)


def create_task(step):
    type = step["type"].lower()
    if type == "tx":        
        return Tx(sock, step["signal"], step["power_level"], step["number_of_loops"], step["sleep_between_loops"], step["fc"])
    elif type == "rx":
        print(str(step))
        return Rx(sock, step["number_of_recs"], step["rec_size"], step["rx_out_folder"], step["rx_out_file"], step["sleep_between_loops"])
    elif type == "txrx":
        return TxRx(sock, step["signal"], step["power_level"], step["number_of_loops"], step["sleep_between_loops"], step["fc"], step["rec_size"], step["rx_out_folder"], step["rx_out_file"])
    elif type == "sendmsg":
        return SendMsg(sock, step["recipient"], step["power_level"], step["text"], step["number_of_loops"],  step["sleep_between_loops"])
    elif type == "getmsg":
        return GetMsg(sock)
    else:
        return None


if __name__ == "__main__":
    check_args()
    load_mission()
    for step in mission_steps:
        step.id()
        step.exec_step()
