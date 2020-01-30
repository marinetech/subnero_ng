# import sys
# import time
# import datetime
# import numpy as np
# import arlpy as ap
# import matplotlib.pyplot as plt
# from matplotlib.pyplot import style
# from matplotlib.pyplot import figure
# from unetpy import *

import arlpy.plot as plt
import numpy as np


signal_file = '/home/ilan/projects/subnero_ng/evdmode/out/rx_out/rx_rec_1'
# signal_file = '/home/ilan/projects/subnero_ng/signals/subnero.sig'
# signal = np.loadtxt(signal_file)
signal = np.loadtxt(signal_file, dtype=complex, converters={0: lambda s: complex(s.decode().replace('+-', '-'))})

plt.plot(signal[:10000].real, fs=19200)


# figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')
# plt.suptitle(signal_file, fontsize=20)
# plt.xlabel('Sample number', fontsize=18)
# plt.ylabel('Amplitude', fontsize=16)
# plt.plot(signal)
# plt.show()
