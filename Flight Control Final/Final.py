import numpy as np
from Vertexes import Vertexes
from Visualizer2 import Visualizer
from Dynamics import Dynamics
from ForcesMoments import ForcesMoments
from Trim import Trim
from Autopilot import Autopilot
from Rotations import Euler2Rotation as rot
import Parameters as p
from Canyon import Canyon as can
from Sensing import Sensing as sen

# AIRCRAFT MODEL VERTEXES
vertexes = Vertexes(p.model)
verts = vertexes.stl_to_vertices() * p.scale
verts = np.matmul(verts, rot(0, 0, -np.pi / 2))

# CALLING CLASSES
fm = ForcesMoments()
dyn = Dynamics()
ap = Autopilot(-50, 10)
trim = Trim()
yon = can(dist=200, ang=20, n=75, h=100, offset=1 / 2)
anim = Visualizer(yon)
# anim.initialization()
n = 4
cr = 350
tune = 900
temp = (-np.arange(n // 2) - 1) * np.pi / 2 / (n // 2)
sA = np.append(temp, np.abs(temp))
margin = 0.52
# TIME INITIALIZATION
t0 = p.t0
t1 = p.t1
ts = p.ts
t = t0

Va = 35
angle = np.pi / 2
radius = np.inf
state, defL = trim.minTrim(Va, angle, radius)

# PPP UVW ANG PQR
state = np.array([[0], [-100], [45],
                  [10], [0], [0],
                  [0], [0], [np.pi / 2],
                  [0], [0], [0]])
dyn.state = np.copy(state)
flag = True
aSens = False
bSens = False
Va_r = 25
h_r = 100
chi_r = np.pi / 2
while t < t1:
    # DISTANCE SENSING
    if dyn.state[1, 0] > 25:
        o = np.array([dyn.state[0, 0], dyn.state[1, 0]])
        psi = dyn.state[8, 0]
        if flag:
            s = sen(sA, o, psi, cr, yon.a, yon.b)
            flag = False
        aSens, bSens, aDist, bDist = s.update(psi, o)
        if p.temp % p.plt == 0:
            if aDist[0] / (aDist[0] + bDist[0]) > margin:
                chi_r -= np.pi / tune
            elif bDist[0] / (aDist[0] + bDist[0]) > margin:
                chi_r += np.pi / tune

            if aDist[1] - bDist[1] > 0:
                chi_r -= np.pi / (tune * 2.5)
            elif aDist[1] - bDist[1] < 0:
                chi_r += np.pi / (tune * 2.5)
            else:
                chi_r = psi

    # SIM UPDATES
    Va = np.sqrt(dyn.state[3, 0] ** 2 + dyn.state[4, 0] ** 2 + dyn.state[5, 0] ** 2)
    u = np.array([t, dyn.state[6, 0], dyn.state[7, 0], dyn.state[8, 0], dyn.state[9, 0], dyn.state[10, 0],
                  dyn.state[11, 0], Va, dyn.state[2, 0], Va_r, h_r, chi_r])
    defL = ap.update(u)
    force, lmn = fm.compute(dyn.state, defL)
    dyn.update(force, lmn)

    # PLOT UPDATES
    if p.temp % p.plt == 0:
        dPack = np.array([Va, Va_r, h_r, chi_r])
        ppp = dyn.state[(0, 1, 2), 0]
        ph, th, ps = dyn.state[(6, 7, 8), 0].flatten()
        r = rot(-ph, th, ps)
        rVerts = np.matmul(r, verts.T).T
        tVerts = rVerts + ppp
        anim.update(tVerts, dyn.state, aSens, bSens)
        # anim.update(tVerts, dyn.state, force, lmn, defL, dPack, t)

    t += ts
    p.temp += 1
