import numpy as np


m = 5.0
k = 3.0
b = 0.5
kp = 4.5
kd = 12.0

z_r = 2

state0 = np.zeros((2, 1))
state0[0, 0] = z_r

t0 = 0
tf = 120
ts = .1
tA = np.arange(t0, tf + ts, ts)

sq = 2.5
