import numpy as np
from control.matlab import *
from MAV import MAV
from Parameters import *


class Transfer:
    def __init__(self):
        self.mav = MAV()
        self.gamma = self.mav.gamma

    def compTF(self, xTrim, uTrim):
        VaTrim = np.sqrt(xTrim[3][0] ** 2 + xTrim[4][0] ** 2 + xTrim[5][0] ** 2)
        aTrim = np.arctan(xTrim[5][0] / xTrim[3][0])
        bTrim = np.arctan(xTrim[4][0] / VaTrim)
        thTrim = xTrim[7][0]

        Cpp = self.gamma[3] * cLp + self.gamma[4] * cNp
        CpDa = self.gamma[3] * cLDa + self.gamma[4] * cNDa

        aPh1 = -.5 * rho * VaTrim ** 2 * S * b * Cpp * (b / (2 * VaTrim))
        aPh2 = .5 * rho * VaTrim ** 2 * S * b * CpDa
        aTh1 = -(rho * VaTrim ** 2 * c * S) / (2 * jy) * cmq * (c / (2 * VaTrim))
        aTh2 = -(rho * VaTrim ** 2 * c * S) / (2 * jy) * cma
        aTh3 = (rho * VaTrim ** 2 * c * S) / (2 * jy) * CpDa

        aV1 = (rho * VaTrim * S / M) * (cd0 + cda * aTrim + cdDe * uTrim[0][0]) + (rho * S_prop) / M * cProp * VaTrim
        aV2 = rho * S_prop / M * cProp * kMotor ** 2 * uTrim[3][0]
        aV3 = g * np.cos(thTrim - aTrim)

        aB1 = -(rho * VaTrim * S) / (2 * M) * cYb
        aB2 = (rho * VaTrim * S) / (2 * M) * cYDr

        tPhDa = tf([aPh2], [1, aPh1, 0])
        tChPh = tf([g / VaTrim], [1, 0])
        tThDe = tf(aTh3, [1, aTh1, aTh2])
        tHTh = tf([VaTrim], [1, 0])
        tHVa = tf([thTrim], [1, 0])
        tVaDt = tf([aV2], [1, aV1])
        tVaTh = tf([-aV3], [1, aV1])
        tBDr = tf([aB2], [1, aB1])

        print('Open Loop Transfer Functions:')
        print('phi Da:', tPhDa)
        print('chi phi:', tChPh)
        print('theta De:', tThDe)
        print('h theta:', tHTh)
        print('beta Dr', tBDr)
        print('Va D:', tVaDt)
        print('Va theta:', tVaTh)
        print('h Va:', tHVa)

        return tPhDa, tChPh, tThDe, tHTh, tHVa, tVaDt, tVaTh, tBDr

    def StateSpace(self, xTrim, uTrim):
        pn, pe, pd, u, v, w, ph, th, ps, p, q, r = xTrim.flatten()
        De, Da, Dr, Dt = uTrim.flatten()

        Va = np.sqrt(u ** 2 + v ** 2 + w ** 2)
        alpha = np.arctan(w / u)
        beta = np.arctan(v / Va)

        cp0 = self.gamma[3] * cL0 + self.gamma[4] * cN0
        cpb = self.gamma[3] * cLb + self.gamma[4] * cNb
        cpp = self.gamma[3] * cLp + self.gamma[4] * cNp
        cpr = self.gamma[3] * cLr + self.gamma[4] * cNr
        cpDa = self.gamma[3] * cLDa + self.gamma[4] * cNDa
        cpDr = self.gamma[3] * cLDr + self.gamma[4] * cNDr
        cr0 = self.gamma[4] * cL0 + self.gamma[8] * cN0
        crb = self.gamma[4] * cLb + self.gamma[8] * cNb
        crp = self.gamma[4] * cLp + self.gamma[8] * cNp
        crr = self.gamma[4] * cLr + self.gamma[8] * cNr
        crDa = self.gamma[4] * cLDa + self.gamma[8] * cNDa
        crDr = self.gamma[4] * cLDr + self.gamma[8] * cNDr

        yv = ((rho * S * v) / (4 * M * Va)) * (cYp * p + cYr * r) + (
                (rho * S * v) / M) * (
                     cY0 + cYb * beta + cYDa * Da + cYDr * Dr) + (
                     (rho * S * cYb) / (2 * M)) * np.sqrt(u ** 2 + w ** 2)
        yp = w + ((rho * Va * S * b) / (4 * M)) * cYp
        yr = -u + ((rho * Va * S * b) / (4 * M)) * cYr
        yDa = ((rho * Va ** 2 * S) / (2 * M)) * cYDa
        yDr = ((rho * Va ** 2 * S) / (2 * M)) * cYDr
        lv = ((rho * S * b ** 2 * v) / (4 * Va)) * (cpp * p + cpr * r) + (
                rho * S * b * v) * (
                     cp0 + cpb * beta + cpDa * Da + cpDr * Dr) + (
                     rho * S * b * cpb / 2) * np.sqrt(u ** 2 + w ** 2)
        lp = self.gamma[1] * q + (rho * Va * S * b ** 2 / 4) * cpp
        lr = -self.gamma[2] * q + (rho * Va * S * b ** 2 / 4) * cpr
        lDa = (rho * Va ** 2 * S * b / 2) * cpDa
        lDr = (rho * Va ** 2 * S * b / 2) * cpDr
        N_v = ((rho * S * b ** 2 * v) / (4 * Va)) * (crp * p + crr * r) + (
                rho * S * b * v) * (
                      cr0 + crb * beta + crDa * Da + crDr * Dr) + (
                      rho * S * b * crb / 2) * np.sqrt(u ** 2 + w ** 2)
        N_p = self.gamma[7] * q + (rho * Va * S * b ** 2 / 4) * crp
        N_r = -self.gamma[1] * q + (rho * Va * S * b ** 2 / 4) * crr
        N_delta_a = (rho * Va ** 2 * S * b / 2) * crDa
        N_delta_r = (rho * Va ** 2 * S * b / 2) * crDr

        cd = cd0 + (cda * alpha)
        cl = cl0 + (cla * alpha)
        cxa = -cda * np.cos(alpha) + cla * np.sin(alpha)
        cx0 = -cd0 * np.cos(alpha) + cl0 * np.sin(alpha)
        cxDe = -cdDe * np.cos(alpha) + clDe * np.sin(alpha)
        cxq = -cdq * np.cos(alpha) + clq * np.sin(alpha)
        cz = -cd * np.sin(alpha) - cl * np.cos(alpha)
        czq = -cdq * np.sin(alpha) - clq * np.cos(alpha)
        czDe = -cdDe * np.sin(alpha) - clDe * np.cos(alpha)
        cz0 = -cd0 * np.sin(alpha) - cl0 * np.cos(alpha)
        cza = - cda * np.sin(alpha) - cla * np.cos(alpha)

        xu = ((u * rho * S) / M) * (cx0 + (cxa * Da) + (cxDe * De)) - (
                (rho * S * w * cxa) / (2 * M)) + (
                     (rho * S * c * cxq * u * q) / (4 * M * Va)) - (
                     (rho * S_prop * cProp * u) / M)
        xw = -q + ((w * rho * S) / M) * (cx0 + (cxa * Da) + (cxDe * De)) + (
                (rho * S * c * cxq * w * q) / (4 * M * Va)) + (
                     (rho * S * u * cxa) / (2 * M)) - (
                     (rho * S_prop * cProp * w) / M)
        xq = -w + ((rho * Va * S * cxq * c) / (4 * M))
        xDe = (rho * (Va ** 2) * S * cxDe) / (2 * M)
        xDt = (rho * S_prop * cProp * (kMotor ** 2) * Dt) / M
        zu = q + ((u * rho * S) / M) * (
                cz0 + (cza * alpha) + (czDe * De)) - (
                     (rho * S * cza * w) / (2 * M)) + (
                     (u * rho * S * czq * c * q) / (4 * M * Va))
        zw = ((w * rho * S) / M) * (cz0 + (cza * alpha) + (czDe * De)) + (
                (rho * S * cza * u) / (2 * M)) + (
                     (w * rho * S * czq * c * q) / (4 * M * Va))
        zq = u + (rho * Va * S * czq * c) / (4 * M)
        zDe = (rho * (Va ** 2) * S * czDe) / (2 * M)
        mu = ((u * rho * S * c) / jy) * (
                cm0 + (cma * alpha) + (cmDe * De)) - (
                     (rho * S * c * cma * w) / (2 * jy)) + (
                     (rho * S * (c ** 2) * cmq * q * u) / (4 * jy * Va))
        mw = ((w * rho * S * c) / jy) * (cm0 + cma * alpha + cmDe * De) + (
                (rho * S * c * cma * u) / (2 * jy)) + (
                     (rho * S * c ** 2 * cmq * q * w) / (4 * jy * Va))
        mq = (rho * Va * c ** 2 * S * cmq) / (4 * jy)
        mDe = (rho * (Va ** 2) * S * c * cmDe) / (2 * jy)

        aLat = np.round(np.array([[yv, yp, yr, g * np.cos(th) * np.cos(ph), 0],
                                  [lv, lp, lr, 0, 0], [N_v, N_p, N_r, 0, 0],
                                  [0, 1, np.cos(ph) * np.tan(th),
                                   q * np.cos(ph) * np.tan(th) - r * np.sin(ph) * np.tan(th), 0],
                                  [0, 0, np.cos(ph) * (1 / np.cos(th)),
                                   p * np.cos(ph) * (1 / np.cos(th)) - r * np.sin(ph) * (1 / np.cos(th)), 0]]),
                        3)
        bLat = np.round(
            np.array([[yDa, yDr], [lDa, lDr], [N_delta_a, N_delta_r], [0, 0], [0, 0]]), 3)

        aLon = np.round(np.array([[xu, xw, xq, -g * np.cos(th), 0],
                                  [zu, zw, zq, -g * np.sin(th), 0],
                                  [mu, mw, mq, 0, 0],
                                  [0, 0, 1, 0, 0],
                                  [np.sin(th), -np.cos(th), 0, u * np.cos(th) + w * np.sin(th), 0]]), 3)

        bLon = np.round(np.array([[xDe, xDt], [zDe, 0], [mDe, 0], [0, 0], [0, 0]]), 3)

        latVal, latVec = np.linalg.eig(aLat)
        lonVal, lonVec = np.linalg.eig(aLon)

        print('Lateral A Matrix:', aLat)
        print('Lateral B Matrix:', bLat)
        print('Longitudinal A Matrix:', aLon)
        print('Longitudinal B Matrix:', bLon)
        print('Lateral Eigenvalues:', latVal)
        print('Longitudinal Eigenvalues:', lonVal)
        print('Short Period Mode:', lonVal[1], lonVal[2])
        print('Phugoid Mode:', lonVal[3], lonVal[4])
        print('Spiral Divergence Mode:', latVal[4])
        print('Roll Mode:', latVal[1])
        print('Dutch Roll Mode:', latVal[2], latVal[3])

        return aLat, bLat
