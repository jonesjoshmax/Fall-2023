import numpy as np
from Vertexes import Vertexes
from Visualizer import Visualizer
from Dynamics import Dynamics
from ForcesMoments import ForcesMoments
from Trim import Trim
from Transfer import Transfer
from Rotations import Euler2Rotation as rot
import Parameters as p

vertexes = Vertexes(p.model)
verts = vertexes.stl_to_vertices() * p.scale
verts = np.matmul(verts, rot(0, 0, np.pi / 2))

fm = ForcesMoments()
dynamics = Dynamics()
animation = Visualizer()
trim = Trim()
tf = Transfer()

# TIME INITIALIZATION
t0 = p.ts
t1 = p.t1
ts = p.ts
t = t0

Va = 13
ang = np.deg2rad(0)
rad = np.inf
state, defL = trim.minTrim(Va, ang, rad)
state = np.array([[state[0, 0]],    # n
                  [state[1, 0]],    # e
                  [state[2, 0]],    # d
                  [state[3, 0]],    # u
                  [state[4, 0]],    # v
                  [state[5, 0]],    # w
                  [state[6, 0]],    # ph
                  [state[7, 0]],    # th
                  [state[8, 0]],    # ps
                  [state[9, 0]],    # p
                  [state[10, 0]],   # q
                  [state[11, 0] + 40]])  # r
tPhDa, tChPh, tThDe, tHTh, tHVa, tVaDt, tVaTh, tBDr = tf.compTF(state, defL)
aLat, bLat = tf.StateSpace(state, defL)
force, lmn = fm.compute(state, defL)
animation.initialization()
dynamics.state = np.copy(state)

while t < t1:
    force, lmn = fm.compute(dynamics.state, defL)
    dynamics.update(force, lmn)

    ppp = dynamics.state[(0, 1, 2), 0]
    ph, th, ps = dynamics.state[(6, 7, 8), 0].flatten()

    if p.temp % p.plt == 0:
        r = rot(-ph, th, ps)
        rVerts = np.matmul(r, verts.T).T
        tVerts = rVerts + ppp
        animation.update(tVerts, dynamics.state, force, lmn, defL)

    t += ts
    p.temp += 1
