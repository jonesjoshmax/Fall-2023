import numpy as np

# GENERAL PARAMETERS
mc = 1.0
mr = 0.25
ml = 0.25
d = 0.3
mu = 0.1
jc = 0.0042
g = 9.81

# GAINS
kd = 0.75
kp = 0.09

# SIM REFS
h_r = 3

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

# TIME PARAMS
t0 = 0.0
tf = 90.0
ts = 0.1
tA = np.arange(t0, tf + ts, ts)

# MAX FORCE INPUT
fMax = 500.0

# PLOTTING VARIABLES
animLim = 10
cSize = 0.25
dSize = cSize / 3
