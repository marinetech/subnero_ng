import sys
import os
import time
import numpy as np
import arlpy as ap
from unetpy import *

import env

class Task:
    def __init__(self, ip_address):
        self.ip_address = ip_address        

        # Open connection to the modem
        print("-I- connecting to modem: " + ip_address)
        try:
            self.modem = UnetGateway(ip_address, 1100)
        except:
            exit(1)



    def exec(self):
        pass
