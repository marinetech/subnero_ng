modem = 'localhost'
port = 1101
recipient = 31 # 0 means broadcast
power_level = -40 # Max:0; Min:-138
number_of_loops = 5
sleep_between_loops = 4 #seconds

#---------------------------------------#
from unetpy import *
import time

s = UnetSocket(modem, port)
for count in range(number_of_loops):
    print()
    print("-I- Sending string #" + str(count+1))
    s.send('hello!', recipient)

    if sleep_between_loops:
        print("-I- sleeping for {} seconds".format(sleep_between_loops))
        time.sleep(sleep_between_loops)
s.close()
