import numpy as np
from vtolParameters import *


class Controller:
    def __init__(self):
        self.z, self.h, self.th, self.zDot, self.hDot, self.thDot = state0.flatten()
        self.sig = sig
        self.intH = 0
        self.intZ = 0.0
        self.erHD1 = 0.0
        self.erZD1 = 0.0
        self.erThDot = 0.0
        self.erHDot = 0.0
        self.erZDot = 0.0
        self.zD1 = 0.0
        self.thD1 = 0.0
        self.hD1 = 0.0

    def update(self, z_r, h_r, state):
        self.z, self.h, self.th, self.zDot, self.hDot, self.thDot = state.flatten()

        t_eq = 0.
        Z = kpZ * (z_r - self.z) - kdZ * self.zDot
        t_c = kpTh * (Z - self.th) - kdTh * self.thDot
        T = t_eq + t_c

        f_eq = g * (mc + 2 * mr)
        f_c = kpH * (h_r - self.h) - kdH * self.hDot
        F = f_eq + f_c

        fr = (T + d * F) / (2 * d)
        fl = F - fr
        fr = self.sat(fr)
        fl = self.sat(fl)
        return fr, fl

    def update2(self, z_r, h_r, state):
        z, h, th, tmp1, tmp2, tmp3 = state.flatten()

        f_fl = g * (mc + 2 * mr)
        erH = h_r - h
        self.intH = self.intH + (ts / 2) * (erH + self.erHD1)
        self.erHDot = beta * self.erHDot + (1 - beta) * ((h - self.hD1) / ts)
        f_tilde = kpH * (h_r - h) + ki * self.intH - kdH * self.erHDot
        f = f_tilde + f_fl

        erZ = z_r - z
        self.intZ = self.intZ + (ts / 2) * (erZ + self.erZD1)
        self.erZDot = beta * self.erZDot + (1 - beta) * ((z - self.zD1) / ts)

        thRUnsat = kpZ * erZ + ki * self.intZ - kdZ * self.erZDot
        thR = self.sat(thRUnsat, thMax)
        erTh = thR - th
        self.erThDot = beta * self.erThDot + (1 - beta) * ((th - self.thD1) / ts)
        tau = kpTh * erTh - kdTh * self.erThDot

        fr = (f + tau / d) / 2
        fl = (f - tau / d) / 2
        fr = self.biSat(fr, fMax, fMin)
        fl = self.biSat(fl, fMax, fMin)

        self.erHD1 = erH
        self.erZD1 = erZ
        self.thD1 = th
        self.zD1 = z
        self.hD1 = h

        return fr, fl

    @staticmethod
    def sat(u, limit):
        if abs(u) > limit:
            u = limit * np.sign(u)
        return u

    @staticmethod
    def biSat(f, up_limit, low_limit):
        if abs(f) > up_limit or abs(f) < low_limit:
            f = up_limit * np.sign(f)
        return f
