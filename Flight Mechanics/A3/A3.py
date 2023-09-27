import numpy as np
from Vertexes import Vertexes
from Visualizer import Visualizer
from Dynamics import Dynamics
from Aerodynamics import Aerodynamics
from Wind import Wind
from Rotations import Euler2Rotation as rot
import Parameters as p
import keyboard

vertexes = Vertexes(p.model)
verts = vertexes.stl_to_vertices() * p.scale

aerodynamics = Aerodynamics()
dynamics = Dynamics()
animation = Visualizer()

# TIME INITIALIZATION
t0 = p.ts
t1 = p.t1
ts = p.ts
t = t0

# INPUT INITIALIZATION
# MATRIX CONTAINING FORCES, [[FX], [FY], [FZ]]
f = np.zeros((3, 1))
# EXTERNAL MOMENTS [[L], [M], [N]]
lmn = np.zeros((3, 1))

# DIFFERENTIAL CONTROL DATA [[Da], [De], [Dr], [Dt]]
defL = p.defL
Da, De, Dr, Dt = defL.flatten()

Va = np.sqrt(p.uvw[0, 0] ** 2 + p.uvw[1, 0] ** 2 + p.uvw[2, 0] ** 2)
wind = Wind()

animation.initialization()
while t < t1:

    if keyboard.is_pressed("l"):
        Da += np.deg2rad(0.5)
        Dr -= np.deg2rad(0.25)
    if keyboard.is_pressed("j"):
        Da -= np.deg2rad(0.5)
        Dr += np.deg2rad(0.25)
    if keyboard.is_pressed("i"):
        De -= np.deg2rad(1)
    if keyboard.is_pressed("k"):
        De += np.deg2rad(1)
    if keyboard.is_pressed("space"):
        De = 0
        Da = 0
        Dr = 0
    if keyboard.is_pressed("shift"):
        if Dt < 1:
            Dt += 0.1
    if keyboard.is_pressed("left control"):
        if Dt > 0:
            Dt -= 0.1

    defL = np.array([[Da], [De], [Dr], [Dt]])

    vab = wind.update(dynamics.h(), Va, ts)
    force = aerodynamics.forces(dynamics.h(), defL, vab)
    lmn = aerodynamics.moments(dynamics.h(), defL, vab)

    dynamics.update(force, lmn)

    ppp = dynamics.h()[(0, 1, 2), 0]
    ph, th, ps = dynamics.h()[(6, 7, 8), 0].flatten()

    # ROTATING STL TO BE CORRECT ORIENTATION
    if t == t0:
        verts = np.matmul(verts, rot(0, 0, -np.pi / 2))

    r = rot(ph, th, ps)
    rVerts = np.matmul(r, verts.T).T
    tVerts = rVerts + ppp

    animation.update(tVerts, dynamics.state, force, lmn, defL)
    t += ts
