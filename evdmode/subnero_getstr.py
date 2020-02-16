modem = 'localhost'
port = 1102
number_of_loops = 5
sleep_between_loops = 0 #seconds

#---------------------------------------#
from unetpy import *
import time

s = UnetSocket(modem, port)
for count in range(number_of_loops):
    print()
    print("-I- waiting for string #" + str(count+1))
    rx = s.receive()
    print('from node', rx.from_, ':', bytearray(rx.data).decode())  

    if sleep_between_loops:
        print("-I- sleeping for {} seconds".format(sleep_between_loops))
        time.sleep(sleep_between_loops)
s.close()
