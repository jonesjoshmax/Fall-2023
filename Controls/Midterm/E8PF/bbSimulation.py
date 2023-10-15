from bbVisualizer import Visualizer
from bbDynamics import Dynamics
from bbController import Controller
from bbParameters import *

vis = Visualizer()
dyn = Dynamics()
con = Controller()
ref = 0.25

plt = 250
temp = plt
t = t0
state = state0

while t < tf:
    r = ref
    f = con.update(r, state)
    state = dyn.update(f)
    if temp % plt == 0:
        vis.update(state, f, r, t)
    t += ts
    temp += 1
