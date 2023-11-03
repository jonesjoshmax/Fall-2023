import numpy as np
from msdController import Controller
from msdDynamics import Dynamics
from msdVisualizer import Visualizer
from signalGenerator import signalGenerator
from msdParameters import *

dyn = Dynamics()
con = Controller()
vis = Visualizer()
ref = signalGenerator(amplitude=z_r, frequency=.0001)

t = t0
state = dyn.state


while t < tf:
    r = ref.square(t)
    f = con.update2(r, state)
    state = dyn.update(f)
    if temp % plot == 0 or temp == 0:
        vis.update(state, f, r, t)
    t += ts
    temp += 1
