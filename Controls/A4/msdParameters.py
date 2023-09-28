import numpy as np


m = 5.0
k = 3.0
b = 0.5
kp = 0.9
kd = 2.4

z_r = 2

state0 = np.zeros((2, 1))

t0 = 0
tf = 120
ts = 0.1
tA = np.arange(t0, tf + ts, ts)
