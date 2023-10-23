import numpy as np
import Rotations as rot
from scipy.optimize import minimize
from math import sin, cos, tan
from ForcesMoments import ForcesMoments
from Dynamics import Dynamics
from MAV import MAV
from Parameters import *


class Trim:
    def __init__(self):
        self.Ts = ts
        self.fm = ForcesMoments()
        self.dyn = Dynamics()
        self.mav = MAV()
        self.gamma = self.mav.gamma

    def costTrim(self, x, Va, Y, R):
        xDot = np.zeros((12, 1))
        xDot[2] = -Va * sin(Y)
        xDot[8] = Va / R

        xTrim, uTrim = self.compTrim(x, Va, Y, R)
        f, lmn = self.fm.compute(xTrim, uTrim)

        stateDot = self.der(xTrim, f, lmn)
        J = np.linalg.norm(xDot - stateDot) ** 2

        return J

    def minTrim(self, Va, Y, R):
        x0 = np.array([0, 0, 0])
        res = minimize(lambda x: self.costTrim(x, Va, Y, R), x0, method='nelder-mead',
                       options={'xatol': 1e-8})
        xTrim, uTrim = self.compTrim(res.x, Va, Y, R)
        return xTrim, uTrim

    def compTrim(self, x, Va, Y, R):
        alpha = x[0]
        beta = x[1]
        phi = x[2]

        theta = alpha + Y

        u = Va * cos(alpha) * cos(beta)
        v = Va * sin(beta)
        w = Va * sin(alpha) * cos(beta)

        p = (-Va / R) * sin(theta)
        q = (Va / R) * sin(phi) * cos(theta)
        r = (Va / R) * cos(phi) * cos(theta)

        xTrim = np.array([[0], [0], [0], [u], [v], [w], [phi], [theta], [0], [p], [q], [r]])

        cl = cl0 + cla * alpha
        cd = cd0 + cda * alpha

        cx = -cd * cos(alpha) + cl * sin(alpha)
        cxq = -cdq * cos(alpha) + clq * sin(alpha)
        cxDe = -cdDe * cos(alpha) + clDe * sin(alpha)

        De = (((jxz * (p ** 2 - r ** 2) + (jx - jz) * p * r) / (
                0.5 * rho * (Va ** 2) * c * S)) - cm0 - cma * alpha - cmq * (
                      (c * q) / (2 * Va))) / cmDe

        Dt = np.sqrt(((2 * mass * (-r * v + q * w + g * sin(theta)) - rho * (Va ** 2) * S *
                       (cx + cxq * ((c * q) / (2 * Va)) + cxDe * De)) /
                      (rho * S_prop * cProp * kMotor ** 2)) + ((Va ** 2) / (kMotor ** 2)))

        diffMat = np.linalg.inv(np.array([[cLDa, cLDr],
                                         [cNDa, cNDr]]))
        magMat = np.array([[((-self.gamma[1] * p * q + self.gamma[2] * q * r) / (
                0.5 * rho * (Va ** 2) * S * b)) - cL0 - cLb * beta - cLp * (
                                    (b * p) / (2 * Va)) - cLr * ((b * r) / (2 * Va))],
                           [((-self.gamma[7] * p * q + self.gamma[1] * q * r) / (
                                   0.5 * rho * (Va ** 2) * S * b)) - cN0 - cNb * beta - cNp * (
                                    (b * p) / (2 * Va)) - cNr * ((b * r) / (2 * Va))]])
        DaDr = np.matmul(diffMat, magMat)

        Da, Dr = -DaDr.flatten()

        uTrim = np.array([[De], [Da], [Dr], [Dt]])

        return xTrim, uTrim

    def der(self, state, f, lmn):
        pn, pe, pd, u, v, w, ph, th, ps, p, q, r = state.flatten()
        l, m, n = lmn.flatten()

        bv = np.array([[u], [v], [w]])
        iv = rot.Euler2Rotation(ph, th, ps) @ bv
        fvb = 1 / mass * f

        pnDot, peDot, pdDot = iv.flatten()

        uvwDot = np.array([[r * v - q * w],
                           [p * w - r * u],
                           [q * u - p * v]]) + fvb
        uDot, vDot, wDot = uvwDot.flatten()

        angVel = np.array([[p], [q], [r]])
        Rgb = np.array([[1, sin(ph) * tan(th), cos(ph) * tan(th)],
                        [0, cos(ph), -sin(ph)],
                        [0, sin(ph) / cos(th), cos(ph) / cos(th)]])
        ptpDot = Rgb @ angVel
        phDot, thDot, psDot = ptpDot.flatten()

        pqrDot = np.array([[self.gamma[1] * p * q - self.gamma[2] * q * r],
                          [self.gamma[5] * p * r - self.gamma[6] * (p ** 2 - r ** 2)],
                          [self.gamma[7] * p * q - self.gamma[1] * q * r]]) + np.array(
            [[self.gamma[3] * l + self.gamma[4] * n],
             [(1 / jy) * m],
             [self.gamma[4] * l + self.gamma[8] * n]])
        pDot, qDot, rDot = pqrDot.flatten()

        xDot = np.array([[pnDot],
                         [peDot],
                         [pdDot],
                         [uDot],
                         [vDot],
                         [wDot],
                         [phDot],
                         [thDot],
                         [psDot],
                         [pDot],
                         [qDot],
                         [rDot],
                         ])
        return xDot
