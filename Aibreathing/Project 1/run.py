import numpy as np
import cycles as c
from graph import graph as g
from params import *

gBPR = g('BPR')
gFPR = g('FPR')
gCPR = g('CPR')


n = 1000
bprArray = np.linspace(bprMin, bprMax, n)
fprArray = np.linspace(fprMin, fprMax, n)
cprArray = np.linspace(cprMin, cprMax, n)

bprData = np.zeros([6, bprArray.size])
for i in range(bprArray.size):
    cycle = c.Ideal(bprIn=bprArray[i])
    # cycle = c.Real(bprIn=bprArray[i])
    bprData[:, i] = cycle.calc()
gBPR.plot(bprData, bprArray)

fprData = np.zeros([6, fprArray.size])
for i in range(fprArray.size):
    cycle = c.Ideal(fprIn=fprArray[i])
    # cycle = c.Real(fprIn=fprArray[i])
    fprData[:, i] = cycle.calc()
gFPR.plot(fprData, fprArray)

cprData = np.zeros([6, cprArray.size])
for i in range(cprArray.size):
    cycle = c.Ideal(cprIn=cprArray[i])
    # cycle = c.Real(cprIn=cprArray[i])
    cprData[:, i] = cycle.calc()
gCPR.plot(cprData, cprArray)
