import numpy as np
from msdController import Controller
from msdDynamics import Dynamics
from msdVisualizer import Visualizer
from signalGenerator import signalGenerator
from msdParameters import *

dyn = Dynamics()
con = Controller()
vis = Visualizer()
ref = signalGenerator(amplitude=z_r, frequency=.03)

t = t0
state = dyn.state

while t < tf:
    r = ref.square(t)
    f = con.update(r, state)
    state = dyn.update(f)
    if temp % plot == 0:
        vis.update(state, f, r)
    t += ts
    temp += 1
