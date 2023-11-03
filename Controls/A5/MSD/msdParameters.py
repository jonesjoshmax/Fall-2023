import numpy as np


m = 5.0 * (1 + (2 * 0.2 * (np.random.rand() - 0.5)))
k = 3.0 * (1 + (2 * 0.2 * (np.random.rand() - 0.5)))
b = 0.5 * (1 + (2 * 0.2 * (np.random.rand() - 0.5)))

d = .7
tr = 2.0
# tr = 1.64    # FASTEST RISE WITH 6 MAX FORCE
w = 2.2 / tr

kd = m * (2 * d * w - b / m)
kp = m * (w ** 2 - k / m)
ki = 0.3

sig = 0.05

fMax = 6

z_r = 1

state0 = np.zeros((2, 1))
# state0[0, 0] = z_r

t0 = 0
tf = 30
ts = .1
tA = np.arange(t0, tf + ts, ts)
plot = 2
temp = 0
pause = 25

sq = 1
