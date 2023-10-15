from bbVisualizer import Visualizer
from bbDynamics import Dynamics
from bbController import Controller
from signalGenerator import signalGenerator
from bbParameters import *

vis = Visualizer()
dyn = Dynamics()
con = Controller()
ref = signalGenerator(amplitude=z_r, frequency=0.025, y_offset=z_o)

plt = 250
temp = plt
t = t0
state = state0

while t < tf:
    r = ref.square(t)
    f = con.update(r, state)
    state = dyn.update(f)
    if temp % plt == 0:
        vis.update(state, f, r, t)
    t += ts
    temp += 1
