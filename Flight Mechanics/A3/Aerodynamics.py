import numpy as np
from Parameters import *


class Aerodynamics:
    def __init__(self):
        self.pn = None
        self.pe = None
        self.pd = None
        self.u = None
        self.v = None
        self.w = None
        self.th = None
        self.ph = None
        self.ps = None
        self.p = None
        self.q = None
        self.r = None
        self.Va = 0
        self.alpha = None
        self.beta = None
        self.Da = None
        self.De = None
        self.Dr = None
        self.Dt = None
        self.wind = None
        self.ts = None
        self.wu = None
        self.wv = None
        self.ww = None
        self.sig = None

    def sigma(self):
        a = 1 + np.exp(-mass * (self.alpha - alpha0)) + np.exp(mass * (self.alpha + alpha0))
        b = (1 + np.exp(-mass * (self.alpha - alpha0))) * (1 + np.exp(mass * (self.alpha + alpha0)))
        self.sig = a / b

    def cla(self):
        return (1 - self.sig) * (cl0 + cla * self.alpha) + self.sig * (2 * np.sign(self.alpha) * np.sin(self.alpha) ** 2
                                                                       * np.cos(self.alpha))

    def cda(self):
        return cdp + (cl0 + cda * self.alpha) ** 2 / (np.pi * e * AR)

    def cxa(self): return -self.cda() * np.cos(self.alpha) + self.cla() * np.sin(self.alpha)

    def cxq(self): return -cdq * np.cos(self.alpha) + clq * np.sin(self.alpha)

    def cxDe(self): return -cdDe * np.cos(self.alpha) + clDe * np.sin(self.alpha)

    def cz(self): return -self.cda() * np.sin(self.alpha) - self.cla() * np.cos(self.alpha)

    def czq(self): return -cdq * np.sin(self.alpha) - clq * np.cos(self.alpha)

    def czDe(self): return -cdDe * np.sin(self.alpha) - clDe * np.cos(self.alpha)

    def update(self, states, data, vab):
        self.Da, self.De, self.Dr, self.Dt = data.flatten()
        self.pn, self.pe, self.pd, self.u, self.v, self.w, self.ph, self.th, self.ps, self.p, self.q, self.r \
            = states.flatten()
        self.Va, self.alpha, self.beta = vab.flatten()
        self.sigma()

    def grav(self):
        grav = np.array([[-mass * g * np.sin(self.th)],
                         [mass * g * np.cos(self.th) * np.sin(self.ph)],
                         [mass * g * np.cos(self.th) * np.sin(self.ph)]])
        return grav

    def aero(self):
        a = rho * (self.Va ** 2) * S / 2
        aero = a * np.array([[self.cxa() + self.cxq() * (c * self.q) / (2 * self.Va) + self.cxDe() * self.De],
                             [cY0 + cYb * self.beta + cYp * (b * self.p) / (2 * self.Va) +
                              cYr * (b * self.r) / (2 * self.Va) + cYDr * self.Dr],
                             [self.cz() + self.czq() * (c * self.q) / (2 * self.Va) + self.czDe() * self.De]])
        return aero

    def prop_f(self):
        a = rho * cProp * cProp / 2
        prop_f = a * np.array([[(kMotor * self.Dt) ** 2 - self.Va ** 2],
                               [0],
                               [0]])
        return prop_f

    def pitch(self):
        a = rho * (self.Va ** 2) * S / 2
        pitch = a * np.array([[b * (cL0 + cLb * self.beta + cLp * (b * self.p) / (2 * self.Va) +
                                    cLr * (b * self.r) / (2 * self.Va) + cLDa * self.Da + cLDr * self.Dr)],
                              [c * (cm0 + cma * self.alpha + cmq * (c * self.q) / (2 * self.Va) + cmDe * self.De)],
                              [b * (cN0 + cNb * self.beta + cNp * (b * self.p) / (2 * self.Va) +
                                    cNr * (b * self.r) / (2 * self.Va) + cNDa * self.Da + cNDr * self.Dr)]])
        return pitch

    def prop_t(self):
        prop_t = np.array([[-kTp * ((kOmega * self.Dt) ** 2)],
                           [0],
                           [0]])
        return prop_t

    def forces(self, states, data, vab):
        self.update(states, data, vab)
        return self.aero() + self.grav() + self.prop_f()

    def moments(self, states, data, vab):
        self.update(states, data, vab)
        return self.pitch() + self.prop_t()
