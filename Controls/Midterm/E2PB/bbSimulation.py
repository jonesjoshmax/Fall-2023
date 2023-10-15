from bbVisualizer import Visualizer
from signalGenerator import signalGenerator
from bbParameters import *
import numpy as np

vis = Visualizer()
z = signalGenerator(amplitude=z_r, frequency=2, y_offset=z_o)
th = signalGenerator(amplitude=.05, frequency=2)

plt = 250
temp = plt
t = t0
state = state0
f = 0
r = 0

while t < tf:
    z_state = z.sin(t)
    th_state = th.sin(t)
    state = np.array([[z_state], [0], [th_state], [0]])
    if temp % plt == 0:
        vis.update(state, f, r, t)
    t += ts
    temp += 1
