import numpy as np
from vtolParameters import *


class Dynamics:
    def __init__(self, alpha=0.0):
        # INITIAL STATE
        self.state = state0

        # TIME STEP
        self.Ts = ts

        # GENERAL PARAMETERS
        self.m = mc
        self.J = jc
        self.mr = mr
        self.ml = ml
        self.d = d
        self.mu = mu

        # FORCES
        self.g = g
        self.fMax = fMax

    def update(self, u):
        u = saturate(u, self.fMax)
        self.rk4_step(u)
        y = self.h()
        return y

    def f(self, state, u):
        z = state[0][0]
        h = state[1][0]
        th = state[2][0]
        zDot = state[3][0]
        hDot = state[4][0]
        thDot = state[5][0]
        fl = u / 2
        fr = u / 2
        # EQUATIONS OF MOTION
        M = np.array([[self.m+2*self.mr, 0, 0],
                      [0, self.m+2*self.mr, 0],
                      [0, 0, self.J+2*self.mr*self.d**2]])
        C = np.array([[-(fr+fl) * np.sin(th) - self.mu * zDot],
                      [(fr+fl) * np.cos(th) - (self.m + 2 * self.mr) * self.g],
                      [self.d*(fr-fl)]])
        tmp = np.linalg.inv(M) @ C
        zDDot = tmp[0][0]
        hDDot = tmp[1][0]
        thDDot = tmp[2][0]
        # RETURN XDOT
        xdot = np.array([[zDot], [hDot], [thDot], [zDDot], [hDDot], [thDDot]])
        return xdot

    def h(self):
        return self.state

    def rk4_step(self, u):
        F1 = self.f(self.state, u)
        F2 = self.f(self.state + self.Ts / 2 * F1, u)
        F3 = self.f(self.state + self.Ts / 2 * F2, u)
        F4 = self.f(self.state + self.Ts * F3, u)
        self.state += self.Ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)

        
def saturate(u, limit):
    shape = np.shape(u)
    u = u.flatten()
    for i in range(len(u)):
        if abs(u[i]) > limit:
            u[i] = limit*np.sign(u[i])
    u = np.reshape(u, shape)
    return u
