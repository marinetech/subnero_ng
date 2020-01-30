import json
import sys
from modules.tx import *


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

    try: #load json file
        with open(sys.argv[1]) as json_file:
            mission = json.load(json_file)
            modem = mission["modem"]
            sock = UnetSocket(modem, 1100)
            for step in mission["steps"]:
                stepObj = create_task(task)
                if stepObj:
                    mission_steps.append(stepObj)
    except Exception as ex:
        print(ex)        
        exit()



def create_task(task):
    type = task["type"].lower()
    if type == "tx":
        try:
            return Tx(task[sock, task["signal"], task["number_of_loops"], task["sleep_between_loops"])
        except KeyError as ex:
            print("KeyError: " + str(ex))
            exit()
    elif type == "rx":
        pass
    else:
        pass


if __name__ == "__main__":
    check_args()
    load_mission()

    
    for task in mission['tasks']:
        mission_steps.append(create_task(task))
