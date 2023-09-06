import numpy as np
import A1P2Parameters as p


class VTOL_Dynamics:
    def __init__(self, alpha=0.0):
        # INITIAL CONDITIONS
        self.state = np.array([
            [p.z0],
            [p.h0],
            [p.th0],
            [p.dz0],
            [p.dh0],
            [p.dth0]
        ])

        self.Ts = p.ts
        # ADDING UNCERTAINTY
        self.mc = p.mc * (1. + alpha * (2. * np.random.rand() - 1.))
        self.mr = p.mr * (1. + alpha * (2. * np.random.rand() - 1.))
        self.ml = p.ml * (1. + alpha * (2. * np.random.rand() - 1.))
        self.jc = p.jc * (1. + alpha * (2. * np.random.rand() - 1.))
        self.d = p.d * (1. + alpha * (2. * np.random.rand() - 1.))
        self.mu = p.mu * (1. + alpha * (2. * np.random.rand() - 1.))

        self.g = p.g
        self.force_limit = p.F_max

    def update(self, ul, ur):
        # TAKES INPUT AT T AND OUTPUTS Y AT T
        # SATURATED FORCE
        ul = saturate(ul, self.force_limit)
        ur = saturate(ur, self.force_limit)
        self.rk4_step(ul, ur)
        return self.h()

    def f(self, state, ul, ur):
        # RETURN xdot = f(x,u)
        z = state[0][0]
        h = state[1][0]
        th = state[2][0]
        dz = state[3][0]
        dh = state[4][0]
        dth = state[5][0]
        fl = ul
        fr = ur

        ddz = (((-fr - fl) * np.sin(th)) - self.mu * dz) / (self.mc + (2 * self.mr))
        ddh = (((fr + fl) * np.cos(th)) - ((self.mc + 2 * self.mr) * self.g)) / (self.mc + (2 * self.mr))
        ddth = self.d * (fr - fl) / (self.jc + (2 * self.mr * self.d * self.d))
        xdot = np.array([[dz], [dh], [dth], [ddz], [ddh], [ddth]])
        return xdot

    def h(self):
        return np.array([self.state[0][0], self.state[1][0], self.state[2][0]])

    def rk4_step(self, ul, ur):
        # RK4 INTEGRATION ALGORITHM
        F1 = self.f(self.state, ul, ur)
        F2 = self.f(self.state + self.Ts / 2 * F1, ul, ur)
        F3 = self.f(self.state + self.Ts / 2 * F2, ul, ur)
        F4 = self.f(self.state + self.Ts * F3, ul, ur)
        self.state += self.Ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)


def saturate(u, limit):
    if abs(u) > limit:
        u = limit * np.sign(u)
    return u
