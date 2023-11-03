import numpy as np

# GENERAL PARAMETERS
mc = 1.0
mr = 0.25
ml = 0.25
d = 0.3
mu = 0.1
jc = 0.0042
g = 9.81

mc = mc * (1 + (2 * 0.2 * (np.random.rand() - 0.5)))
d = d * (1 + (2 * 0.2 * (np.random.rand() - 0.5)))
mu = mu * (1 + (2 * 0.2 * (np.random.rand() - 0.5)))
jc = jc * (1 + (2 * 0.2 * (np.random.rand() - 0.5)))

# TIME PARAMS
t0 = 0.0
tf = 90.0
ts = 0.001
tA = np.arange(t0, tf + ts, ts)
plot = 100
temp = 0
pause = 25

# GAINS
trH = 2
trTh = 0.1
trZ = 1.5
dH = 0.707
dTh = 0.707
dZ = 0.707
wH = 2.2 / trH
wTh = 2.2 / trTh
wZ = 2.2 / trZ

ki = 0.01

kdH = (mc + 2 * mr) * (2 * dH * wH)
kpH = (mc + 2 * mr) * wH ** 2

kdTh = 2 * wTh * dTh * (jc + 2 * mr * d ** 2)
kpTh = wTh ** 2 * (jc + 2 * mr * d ** 2)
kdcTh = kpTh / kpTh

kdZ = (2 * wZ * dZ * (mc + 2 * mr) - mu) / -(g * (mc + 2 * mr) * kdcTh)
kpZ = wZ ** 2 * (mc + 2 * mr) / -(g * (mc + 2 * mr) * kdcTh)

sig = 0.05
beta = (2.0 * sig - ts) / (2.0 * sig + ts)

# INITIAL VALUES
z0 = 0.0
h0 = 0.0
th0 = 0.0
zDot0 = 0.0
hDot0 = 0.0
thDot0 = 0.0

state0 = np.array([[z0],
                   [h0],
                   [th0],
                   [zDot0],
                   [hDot0],
                   [thDot0]])

# MAX FORCE INPUT
fMax = 10.0
fMin = 0
thMax = np.deg2rad(30)

# PLOTTING VARIABLES
animLim = 15
cSize = 0.25
dSize = cSize / 3
