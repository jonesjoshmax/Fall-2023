import matplotlib.pyplot as plt
import numpy as np
import A1P2Parameters as p
from signalGenerator import signalGenerator
from A1P2Visualizer import Visualizer
from A1P2Dynamics import VTOL_Dynamics

# CLASS INITIALIZATION
dynamics = VTOL_Dynamics(alpha=0.0)
reference = signalGenerator(amplitude=0.5, frequency=0.02)
force_L = signalGenerator(amplitude=10, frequency=0.5)
force_R = signalGenerator(amplitude=10, frequency=0.5)
animation = Visualizer()

force_vary = 0.0

# SIMULATION LOOP
t = p.t0
n = 0
f_gain = 1.155
f = 0
while True:
    t_next_plot = t + p.t_plot
    while t < t_next_plot:
        r = reference.square(t)
        ul = f_gain * np.abs(force_R.sin(t))
        ur = f_gain * np.abs(force_L.sin(t))
        if p.t1 / 3 <= t < p.t1 * 2 / 3:
            force_vary = .00005
            ul = (f_gain + force_vary) * np.abs(force_L.sin(t))
            ur = f_gain * np.abs(force_R.sin(t))
        elif p.t1 * 2 / 3 <= t:
            force_vary = .0001
            ul = f_gain * np.abs(force_R.sin(t))
            ur = (f_gain + force_vary) * np.abs(force_L.sin(t))
        y = dynamics.update(ul, ur)
        f = [ul, ur]
        t += p.ts
        if p.t1 - 5 * p.ts <= t <= p.t1 + 5 * p.ts:
            n += 1

    animation.update(dynamics.state, f)
    plt.pause(p.ts)

