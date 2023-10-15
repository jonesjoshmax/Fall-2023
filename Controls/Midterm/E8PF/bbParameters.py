import numpy as np

# GIVEN PHYSICAL PARAMETERS
m1 = 0.35  # kg
m2 = 2.00  # kg
l = 0.5  # m
g = 9.8  # m/s^2

# CONTROLLER VALUES
f_max = 15
z_r = .15
z_o = .25

# GAINS
constant = 3 * l / (m2 * pow(l, 2) + 3 * m1 * pow(l / 2, 2))
tr1 = 1
tr2 = 2.1
w1 = 2.2 / tr1
w2 = 2.2 / tr2
damp = 0.707

c1 = 2 * damp * w1
c2 = pow(w1, 2)

c3 = 2 * damp * w2
c4 = pow(w2, 2)

kd_th = c1 / constant
kp_th = c2 / constant

kd_z = c3 / -g
kp_z = c4 / -g

# INITIAL STATES
z0 = 0.0
zDot0 = 0.0
th0 = 0.0
thDot0 = 0.0
state0 = np.array([[z0], [zDot0], [th0], [thDot0]])

# SIMULATION PARAMETERS
t0 = 0.0
tf = 90.0
ts = 0.0001

# GRAPHING PARAMS
win = 1.0
radius = 0.05  # m
