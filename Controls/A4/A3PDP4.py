import numpy as np
from msdController import Controller
from msdDynamics import Dynamics
from msdVisualizer import Visualizer
from signalGenerator import signalGenerator
from msdParameters import *

dyn = Dynamics()
con = Controller()
vis = Visualizer()
ref = signalGenerator(amplitude=z_r, frequency=.03, y_offset=3*z_r)

t = t0
state = dyn.state

while t < tf:
    r = ref.square(t)
    f = con.update(r, state)
    state = dyn.update(f)
    vis.update(state, f, r)
    t += ts
