import numpy as np
from Parameters import ts
import AutoGains as Ga


class Autopilot:
    def __init__(self, altTOZone, altHZone):
        self.altTOZone = altTOZone
        self.altHZone = altHZone
        self.initInt = 1.0
        self.altState = 0.0

        self.rollInt = 0.0
        self.rollDif = 0.0
        self.rollED1 = 0.0

        self.courseInt = 0.0
        self.courseDif = 0.0
        self.courseED1 = 0.0

        self.pitchInt = 0.0
        self.pitchDif = 0.0
        self.pitchED1 = 0.0

        self.ahpInt = 0.0
        self.ahpDif = 0.0
        self.ahpED1 = 0.0

        self.ahtInt = 0.0
        self.ahtDif = 0.0
        self.ahtED1 = 0.0

        self.ahInt = 0.0
        self.ahDif = 0.0
        self.ahED1 = 0.0

    def update(self, u):
        thC = 0
        dT = 0
        t, ph, th, ch, p, q, r, Va, h, VaC, hC, chC = u.flatten()
        h = -h
        hC = -hC

        # LATERAL AUTOPILOT
        if t == 0:
            dR = 0
            phC = self.cHold(chC, ch, r, 1)
            dA = self.rHold(phC, ph, p, 1)
        else:
            dR = 0
            phC = self.cHold(chC, ch, r, 0)
            dA = self.rHold(phC, ph, p, 0)

        # LONGITUDINAL AUTOPILOT
        if t == 0:
            if h <= self.altTOZone:
                self.altState = 0
            elif h <= hC - self.altHZone:
                self.altState = 1
            elif h >= hC + self.altHZone:
                self.altState = 2
            else:
                self.altState = 3
            self.initInt = 1.0

        if self.altState == 0:
            dT = 1
            thC = 10 * (np.pi / 180)
            if h >= self.altTOZone:
                self.altState = 1
                self.initInt = 1.0
            else:
                self.initInt = 0.0
        elif self.altState == 1:
            dT = 1
            thC = self.asHoldP(VaC, Va, self.initInt)

            if h >= hC - self.altTOZone:
                self.altState = 3
                self.initInt = 1.0
            elif h <= self.altTOZone:
                self.altState = 0
                self.initInt = 1.0
            else:
                self.initInt = 0.0
        elif self.altState == 2:
            dT = 0
            thC = self.asHoldP(VaC, Va, self.initInt)
            if h <= hC + self.altHZone:
                self.altState = 3
                self.initInt = 1.0
            else:
                self.initInt = 0.0
        elif self.altState == 3:
            dT = self.asHoldThr(VaC, Va, self.initInt)
            thC = self.altHold(hC, h, self.initInt)
            if h <= hC - self.altHZone:
                self.altState = 1
                self.initInt = 1.0
            elif h >= hC + self.altHZone:
                self.altState = 2
                self.initInt = 1.0
            else:
                self.initInt = 0.0

        if t == 0:
            dE = self.pHold(thC, th, q, 1)
        else:
            dE = self.pHold(thC, th, q, 0)

        return np.array([[dE], [dA], [dR], [dT]])

    def rHold(self, phC, ph, p, flag):
        upper = np.deg2rad(45)
        lower = -np.deg2rad(45)
        error = phC - ph

        kp = Ga.kpRoll
        kd = Ga.kdRoll
        ki = Ga.kiRoll

        if flag == 1:
            self.rollInt = 0
            self.rollDif = 0
            self.rollED1 = 0

        self.rollInt = self.rollInt + (ts / 2) * (error + self.rollED1)
        self.rollDif = p
        self.rollED1 = error

        u = kp * error + ki * self.rollInt + kd * self.rollDif

        uSat = self.sat(u, upper, lower)
        if ki != 0:
            self.rollInt = self.rollInt + ts / ki * (uSat - u)

        return uSat

    def cHold(self, ch_r, ch, r, flag):
        upper = np.deg2rad(25)
        lower = -np.deg2rad(25)
        error = ch_r - ch

        kd = Ga.kdCourse
        kp = Ga.kpCourse
        ki = Ga.kiCourse

        if flag == 1:
            self.courseInt = 0
            self.courseDif = 0
            self.courseED1 = 0

        self.courseInt = self.courseInt + (ts / 2) * (error + self.courseED1)
        self.courseDif = r
        self.courseED1 = error

        u = kp * error + ki * self.courseInt + kd * self.courseDif

        uSat = self.sat(u, upper, lower)
        if ki != 0.0:
            self.courseInt = self.courseInt * ts / ki * (uSat - u)

        return u

    def pHold(self, th_r, th, q, flag):
        upper = np.deg2rad(45)
        lower = -np.deg2rad(45)
        error = th_r - th

        kd = Ga.kdPitch
        kp = Ga.kpPitch
        ki = Ga.kiPitch

        if flag == 1:
            self.pitchInt = 0
            self.pitchDif = 0
            self.pitchED1 = 0

        self.pitchInt = self.pitchInt + (ts / 2) * (error - self.pitchED1)
        self.pitchDif = q
        self.pitchED1 = error

        u = kp * error + ki * self.pitchInt + kd * self.pitchDif

        uSat = self.sat(u, upper, lower)
        if ki != 0:
            self.pitchInt = self.pitchInt + ts / ki * (uSat - u)

        return uSat

    def altHold(self, h_r, h, flag):
        upper = np.deg2rad(45)
        lower = -np.deg2rad(45)
        tau = 5.0
        error = h_r - h

        kd = Ga.kdAlt
        kp = Ga.kpAlt
        ki = Ga.kiAlt

        if flag == 1:
            self.ahInt = 0
            self.ahDif = 0
            self.ahED1 = 0

        self.ahInt = self.ahInt + (ts / 2) * (error + self.ahED1)
        self.ahDif = (2 * tau - ts) / (2 * tau + ts) * self.ahDif + 2 / (2 * tau + ts) * (
                error - self.ahED1)
        self.ahED1 = error

        u = kp * error + ki * self.ahInt + kd * self.ahDif
        uSat = self.sat(u, upper, lower)

        if ki != 0.0:
            self.ahInt = self.ahInt + ts / ki * (uSat - u)

        return uSat

    def asHoldP(self, va_r, va, flag):
        upper = np.deg2rad(45)
        lower = -np.deg2rad(45)
        tau = 5.0
        error = va_r - va

        kd = Ga.kdVa
        kp = Ga.kpVa
        ki = Ga.kiVa

        if flag == 1:
            self.ahpInt = 0
            self.ahpDif = 0
            self.ahpED1 = 0

        self.ahpInt = self.ahpInt + (ts / 2) * (error + self.ahpED1)
        self.ahpDif = (2 * tau - ts) / (2 * tau + ts) * self.ahpDif + 2 / (2 * tau + ts) * (
                    error - self.ahpED1)
        self.ahpED1 = error

        u = kp * error + ki * self.ahpInt + kd * self.ahpDif
        uSat = self.sat(u, upper, lower)

        if ki != 0.0:
            self.ahpInt = self.ahpInt + ts / ki * (uSat - u)

        return u

    def asHoldThr(self, va_r, va, flag):
        upper = 1.0
        lower = 0.0
        tau = 5.0
        error = va_r - va

        kd = Ga.kdThr
        kp = Ga.kpThr
        ki = Ga.kiThr

        if flag == 1:
            self.ahtInt = 0
            self.ahtDif = 0
            self.ahtED1 = 0

        self.ahtInt = self.ahtInt + (ts / 2) * (error + self.ahtED1)
        self.ahtDif = (2 * tau - ts) / (2 * tau + ts) * self.ahtDif + 2 / (2 * tau + ts) * (
                    error - self.ahtED1)
        self.ahtED1 = error

        u = kp * error + ki * self.ahtInt + kd * self.ahtDif

        uSat = self.sat(u, upper, lower)
        if ki != 0:
            self.ahtInt = self.ahtInt + ts / ki * (uSat - u)

        return uSat

    @staticmethod
    def sat(u, MAX, MIN):
        if u > MAX:
            out = MAX
        elif u < MIN:
            out = MIN
        else:
            out = u
        return out
