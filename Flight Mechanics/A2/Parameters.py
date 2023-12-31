from numpy import zeros
from numpy import arange
from numpy import pi

# MODEL SETTING
model = 'f22.stl'

# TIME SETTINGS
t0 = 0
t1 = 2 * pi
ts = 0.01
t_array = arange(t0, t1 + ts, ts)
freq1 = 6
freq2 = 6
amp1 = 2000
amp2 = 25

# INERTIAL PARAMETERS
jx = 0.824
jy = 1.135
jz = 1.759
# jxz = 0.120
jxz = 0
gravity = 9.806650
mass = 13.5

# INITIAL CONDITIONS
# MATRIX CONTAINING ANGLES, [[PHI], [THETA], [PSI]]
ang = zeros((3, 1))
# MATRIX CONTAINING PN PE PD, [[PN], [PE], [PD]]
pDir = zeros((3, 1))
# MATRIX CONTAINING UVW, [[U], [V], [W]]
uvw = zeros((3, 1))
# MATRIX CONTAINING FORCES, [[FX], [FY], [FZ]]
f = zeros((3, 1))
# EXTERNAL MOMENTS [[L], [M], [N]]
lmn = zeros((3, 1))
# MATRIX CONTAINING PQR, [[P], [Q], [R]]
pqr = zeros((3, 1))

# AERODYNAMIC PARAMETERS
S_wing = 0.55
b = 2.90
c = 0.19
S_prop = 0.2027
rho = 1.2682
e = 0.9
AR = b ** 2 / S_wing
C_L_0 = 0.23
C_D_0 = 0.043
C_m_0 = 0.0135
C_L_alpha = 5.61
C_D_alpha = 0.030
C_m_alpha = -2.74
C_L_q = 7.95
C_D_q = 0.0
C_m_q = -38.21
C_L_delta_e = 0.13
C_D_delta_e = 0.0135
C_m_delta_e = -0.99
M = 50
alpha0 = 0.47
epsilon = 0.16
C_D_p = 0.0
C_Y_0 = 0.0
C_ell_0 = 0.0
C_n_0 = 0.0
C_Y_beta = -0.98
C_ell_beta = -0.13
C_n_beta = 0.073
C_Y_p = 0.0
C_ell_p = -0.51  # ell=p
C_n_p = -0.069
C_Y_r = 0.0
C_ell_r = 0.25
C_n_r = -0.095
C_Y_delta_a = 0.075
C_ell_delta_a = 0.17
C_n_delta_a = -0.011
C_Y_delta_r = 0.19
C_ell_delta_r = 0.0024
C_n_delta_r = -0.069
C_prop = 1
k_motor = 80  # 80
