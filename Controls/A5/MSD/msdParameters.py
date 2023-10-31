import numpy as np


m = 5.0
k = 3.0
b = 0.5

d = 0.7
tr = 1.64
w = 2.2 / tr

kd = m * (2 * d * w - b / m)
kp = m * (w ** 2 - k / m)

fMax = 6

z_r = 1

state0 = np.zeros((2, 1))
# state0[0, 0] = z_r

t0 = 0
tf = 6
ts = .1
tA = np.arange(t0, tf + ts, ts)
plot = 1
temp = plot

sq = 2.5
