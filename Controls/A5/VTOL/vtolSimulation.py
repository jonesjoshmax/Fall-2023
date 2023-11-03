from vtolController import Controller
from vtolDynamics import Dynamics
from vtolVisualizer import Visualizer
from signalGenerator import signalGenerator
from vtolParameters import *

dyn = Dynamics()
con = Controller()
vis = Visualizer()
z_ref = signalGenerator(amplitude=2.5, frequency=.08)
h_ref = signalGenerator(amplitude=2.5, frequency=.04, y_offset=2.5)

t = t0
while t < tf:
    z_r = z_ref.square(t)
    h_r = h_ref.square(t)
    fr, fl = con.update2(z_r, h_r, dyn.state)
    state = dyn.update(fr, fl)
    if temp % plot == 0 or temp == 0:
        f = np.array([[fr], [fl]])
        r = np.array([[z_r], [h_r]])
        vis.update(state, f, r, t)
    t += ts
    temp += 1
