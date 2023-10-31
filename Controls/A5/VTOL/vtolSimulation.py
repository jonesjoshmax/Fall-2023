from vtolController import Controller
from vtolDynamics import Dynamics
from vtolVisualizer import Visualizer
from signalGenerator import signalGenerator
from vtolParameters import *

dyn = Dynamics()
con = Controller()
vis = Visualizer()
ref = signalGenerator(amplitude=h_r, frequency=.015, y_offset=h_r)

t = t0
state = dyn.state

while t < tf:
    r = ref.square(t)
    f = con.update(r, state)
    state = dyn.update(f)
    vis.update(state, f, r)
    t += ts
