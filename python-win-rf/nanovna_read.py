import numpy as np
import skrf as rf
from pylab import *

from nanovna import NanoVNA


def fetch_2_RI():
    nv = NanoVNA()
    print(nv)
    nv.fetch_frequencies()
    f1 = nv.frequencies
    f2 = rf.Frequency.from_f(f1, unit='hz')
    tmp = nv.data(0)
    s11 = s22 = tmp
    tmp = nv.data(1)
    s21 = s12 = tmp
    # s = np.zeros((len(f1), 2, 2))
    s = np.ndarray((len(f1),2,2), complex)
    s[:, 0, 0] = s11
    s[:, 1, 0] = s21
    s[:, 1, 1] = s22
    s[:, 0, 1] = s12
    ntw = rf.Network(frequency=f2, s=s)
    nv.close()
    return ntw
