import numpy as np
from Rotations import Body2Inertial as B2I
import control.matlab as mat


class Wind:

    def __init__(self):
        self.Vs = np.array([[5], [3], [2]])

    @staticmethod
    def drydenGust(Va, t):
        # WHITE NOISE
        su = np.random.normal(0, 1, 1)[0]
        sv = np.random.normal(0, 1, 1)[0]
        sw = np.random.normal(0, 1, 1)[0]

        # DRYDEN PARAMETERS
        Lu = 200
        Lv = 200
        Lw = 50
        ou = ov = 1.06
        ow = 0.7

        # TFT COEFFS
        c1 = ou * np.sqrt(2 * Va / Lu)
        c2 = ov * np.sqrt(3 * Va / Lv)
        c3 = ow * np.sqrt(3 * Va / Lw)

        # TFTS
        hu = mat.tf([0, c1], [1, Va / Lu])
        hv = mat.tf([c2, c2 * Va / (np.sqrt(3) * Lv)], [1, 2 * Va / Lv, (Va / Lv) ** 2])
        hw = mat.tf([c3, c3 * Va / (np.sqrt(3) * Lw)], [1, 2 * Va / Lw, (Va / Lw) ** 2])

        # GUSTS FROM TFTS
        T = [0, t]
        uwg, _, _ = mat.lsim(hu, su, T)
        vwg, _, _ = mat.lsim(hv, sv, T)
        wwg, _, _ = mat.lsim(hw, sw, T)

        return np.array([[uwg[1]], [vwg[1]], [wwg[1]]])

    def update(self, state, Va, ts):
        pn, pe, pd, u, v, w, ph, th, ps, p, q, r = state.flatten()
        gusts = self.drydenGust(Va, ts)
        wind0 = np.matmul(B2I(ph, th, ps), self.Vs) + gusts
        Var = np.array([[u - wind0[0][0]],
                        [v - wind0[1][0]],
                        [w - wind0[2][0]]])
        ur, vr, wr = Var.flatten()
        Va = np.sqrt(ur ** 2 + vr ** 2 + wr ** 2)
        alpha = np.arctan(wr / ur)
        beta = np.arcsin(vr / Va)

        return np.array([Va, alpha, beta])
