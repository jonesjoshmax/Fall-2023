import numpy as np
from MAV import MAV
import Parameters as p
mav = MAV()


class Dynamics:
    def __init__(self):
        self.temp = None
        self.ang = p.ang
        self.pDir = p.pDir
        self.uvw = p.uvw
        self.force = p.f
        self.lmn = p.lmn
        self.pqr = p.pqr
        self.state = np.vstack((self.pDir, self.uvw, self.ang, self.pqr))
        self.ts = p.ts

    def update(self, force, lmn):
        self.rk4_step(force, lmn)
        y = self.h()
        return y

    def f(self, state, force, lmn):
        self.temp = None
        uvw = np.array([[state[3, 0]], [state[4, 0]], [state[5, 0]]])
        ang = np.array([[state[6, 0]], [state[7, 0]], [state[8, 0]]])
        pqr = np.array([[state[9, 0]], [state[10, 0]], [state[11, 0]]])

        pppDot = mav.pppDot(uvw, ang)
        uvwDot = mav.uvwDot(pqr, uvw, force)
        angDot = mav.angDot(pqr, ang)
        pqrDot = mav.pqrDot(pqr, lmn)

        # FIRST ORDER DIFFERENTIALS TO RETURN
        xdot = np.array([[pppDot[0, 0]], [pppDot[1, 0]], [pppDot[2, 0]],
                         [uvwDot[0, 0]], [uvwDot[1, 0]], [uvwDot[2, 0]],
                         [angDot[0, 0]], [angDot[1, 0]], [angDot[2, 0]],
                         [pqrDot[0, 0]], [pqrDot[1, 0]], [pqrDot[2, 0]]])

        return xdot

    def h(self):
        y = self.state

        return y

    def rk4_step(self, force, lmn):
        # RK4 INTEGRATION
        F1 = self.f(self.state, force, lmn)
        F2 = self.f(self.state + self.ts / 2 * F1, force, lmn)
        F3 = self.f(self.state + self.ts / 2 * F2, force, lmn)
        F4 = self.f(self.state + self.ts * F3, force, lmn)
        self.state += self.ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)
