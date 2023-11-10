import numpy as np
from Vertexes import Vertexes
from Visualizer import Visualizer
from Dynamics import Dynamics
from ForcesMoments import ForcesMoments
from Trim import Trim
from Autopilot import Autopilot
from Rotations import Euler2Rotation as rot
import Parameters as p

vertexes = Vertexes(p.model)
verts = vertexes.stl_to_vertices() * p.scale
verts = np.matmul(verts, rot(0, 0, -np.pi / 2))

fm = ForcesMoments()
dyn = Dynamics()
ap = Autopilot(50, 10)
anim = Visualizer()
trim = Trim()

# TIME INITIALIZATION
t0 = p.t0
t1 = p.t1
ts = p.ts
t = t0

Va = 35
angle = np.deg2rad(0)
radius = np.inf
state, defL = trim.minTrim(Va, angle, radius)

anim.initialization()
dyn.state = np.copy(state)

while t < t1:
    if t <= 100:
        Va_r = 30
        h_r = 100
        chi_r = np.deg2rad(0)
    elif 100 < t <= 200:
        Va_r = 45
        h_r = 200
        chi_r = np.deg2rad(30)
    else:
        Va_r = 60
        h_r = 300
        chi_r = np.deg2rad(-30)
    Va = np.sqrt(dyn.state[3, 0] ** 2 + dyn.state[4, 0] ** 2 + dyn.state[5, 0] ** 2)

    u = np.array([t, dyn.state[6, 0], dyn.state[7, 0], dyn.state[8, 0], dyn.state[9, 0], dyn.state[10, 0],
                 dyn.state[11, 0], Va, dyn.state[2, 0], Va_r, h_r, chi_r])
    defL = ap.update(u)

    force, lmn = fm.compute(dyn.state, defL)
    dyn.update(force, lmn)

    if p.temp % p.plt == 0:
        dPack = np.array([Va, Va_r, h_r, chi_r])
        ppp = dyn.state[(0, 1, 2), 0]
        ph, th, ps = dyn.state[(6, 7, 8), 0].flatten()
        r = rot(-ph, th, ps)
        rVerts = np.matmul(r, verts.T).T
        tVerts = rVerts + ppp
        anim.update(tVerts, dyn.state, force, lmn, defL, dPack, t)

    t += ts
    p.temp += 1
