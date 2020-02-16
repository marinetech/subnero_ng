modem = 'localhost'
port = 1101
recipient = 111 # 0 means broadcast
power_level = -40 # Max:0; Min:-138
file_to_send = "abc.txt"

#----------------------------------------------------------#

from unetpy import *
import time

sock = UnetSocket(modem, port)

remote = sock.agentForService(Services.REMOTE)
remote.enable = True
remote << RemoteFilePutReq(to=recipient, filename=file_to_send)


sock.close()
