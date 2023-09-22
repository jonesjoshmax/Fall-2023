import numpy as np
from Vertexes import Vertexes
from Visualizer import Visualizer
from Dynamics import Dynamics
from Aerodynamics import Aerodynamics
from Rotations import Euler2Rotation as rot
import Parameters as p

vertexes = Vertexes(p.model)
verts = vertexes.stl_to_vertices()

aerodynamics = Aerodynamics()
dynamics = Dynamics()
animation = Visualizer()

# TIME INITIALIZATION
t0 = p.ts
t1 = p.t1
ts = p.ts
t = t0
t_array = p.t_array
f_count = t_array.size

# SIGNAL PARAMETERS
freq1 = p.freq1
freq2 = p.freq2
amp1 = p.amp1
amp2 = p.amp2

# INPUT INITIALIZATION
# MATRIX CONTAINING FORCES, [[FX], [FY], [FZ]]
f = np.zeros((3, 1))
# EXTERNAL MOMENTS [[L], [M], [N]]
lmn = np.zeros((3, 1))

data = np.zeros((4, 1))

animation.initialization()
while t < t1:
    #data[0, 0] = 2 * np.abs(np.sin(t))
    #data[1, 0] = 2 * np.abs(np.sin(t))
    #data[2, 0] = 2 * np.abs(np.sin(t))
    #data[3, 0] = 2 * np.abs(np.sin(t))

    force = aerodynamics.forces(dynamics.h(), data, ts)
    lmn = aerodynamics.moments(dynamics.h(), data, ts)

    dynamics.update(force, lmn)

    ppp = dynamics.h()[(0, 1, 2), 0].reshape(3, 1)
    uvw = dynamics.h()[(3, 4, 5), 0].reshape(3, 1)
    ang = dynamics.h()[(6, 7, 8), 0].reshape(3, 1)
    pqr = dynamics.h()[(9, 10, 11), 0].reshape(3, 1)

    if t == t0:
        verts = np.matmul(verts, rot(0, 0, -np.pi / 2))

    rotation = rot(ang[0, 0], ang[1, 0], ang[2, 0])
    pqr2ref = np.dot(rotation, pqr)
    translation = np.rot90((pqr2ref + ppp))
    tempVerts = verts + translation
    for i in range(tempVerts.shape[0]):
        tempVerts[i, :] = np.dot(rotation, tempVerts[i, :])
    animation.update(tempVerts, dynamics.state, force, lmn)
    t += ts

