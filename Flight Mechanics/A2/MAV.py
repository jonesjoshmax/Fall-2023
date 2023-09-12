from numpy import cos as c
from numpy import sin as s
from numpy import tan as t
from numpy import matrix
from numpy import zeros
from numpy import dot
import Parameters as p


class MAV:
    def __init__(self):
        # INITIALIZING VARIABLES
        self.ang = p.ang
        self.pDir = p.pDir
        self.uvw = p.uvw
        self.f = p.f
        self.lmn = p.lmn
        self.pqr = p.pqr

        # MASS
        self.mass = p.mass

        # INERTIAL VALUES
        self.jx = p.jx
        self.jy = p.jy
        self.jz = p.jz
        self.jxz = p.jxz

        # SETUP SCRIPT FOR GAMMA EQUATIONS
        self.gamma = zeros(9)
        self.gamma[0] = self.jx * self.jz - pow(self.jxz, 2)
        self.gamma[1] = self.jxz * (self.jx - self.jy + self.jz) / self.gamma[0]
        self.gamma[2] = (self.jz * (self.jz - self.jy) + self.jxz ** 2) / self.gamma[0]
        self.gamma[3] = self.jz / self.gamma[0]
        self.gamma[4] = self.jxz / self.gamma[0]
        self.gamma[5] = (self.jz - self.jx) / self.jy
        self.gamma[6] = self.jxz / self.jy
        self.gamma[7] = (self.jx * (self.jx - self.jy) + pow(self.jxz, 2)) / self.gamma[0]
        self.gamma[8] = self.jx / self.gamma[0]

    def pppDot(self, uvw, ang):
        # TRANSLATION KINEMATICS
        self.uvw = uvw
        self.ang = ang
        ph = self.ang[0, 0]
        th = self.ang[1, 0]
        ps = self.ang[2, 0]
        a = matrix([[c(th) * c(ps), s(ph) * s(th) * c(ps) - c(ph) * s(ps), c(ph) * s(th) * c(ps) + s(ph) * s(ps)],
                    [c(th) * s(ps), s(ph) * s(th) * s(ps) + c(ph) * c(ps), c(ph) * s(th) * s(ps) - s(ph) * c(ps)],
                    [-s(th), s(ph) * c(th), c(ph) * c(th)]])
        # RETURNS PNdot PEdot PDdOT
        pppDot = dot(a, self.uvw)
        return pppDot

    def uvwDot(self, pqr, uvw, force):
        # ROTATIONAL KINEMATICS
        p = pqr[0, 0]
        q = pqr[1, 0]
        r = pqr[2, 0]
        u = uvw[0, 0]
        v = uvw[1, 0]
        w = uvw[2, 0]
        self.f = force
        a = matrix([[r * v - q * w],
                    [p * w - r * u],
                    [q * u - p * v]
                    ])
        # RETURNS Udot VdOT Wdot
        uvwDot = a + self.f / self.mass
        return uvwDot

    def angDot(self, pqr, ang):
        # TRANSLATIONAL DYNAMICS
        self.pqr = pqr
        self.ang = ang
        ph = self.ang[0, 0]
        th = self.ang[1, 0]
        a = matrix([[1, s(ph) * t(th), c(ph) * t(th)],
                    [0, c(ph), -s(ph)],
                    [0, s(ph) / c(th), c(ph) / c(th)]])
        # RETURNS PHIdot THETAdot PSIdot
        angDot = dot(a, self.pqr)
        return angDot

    def pqrDot(self, pqr, lmn):
        # ROTATIONAL DYNAMICS
        self.pqr = pqr
        self.lmn = lmn
        p = self.pqr[0, 0]
        q = self.pqr[1, 0]
        r = self.pqr[2, 0]
        l = self.lmn[0, 0]
        m = self.lmn[1, 0]
        n = self.lmn[2, 0]
        g1 = self.gamma[1]
        g2 = self.gamma[2]
        g3 = self.gamma[3]
        g4 = self.gamma[4]
        g5 = self.gamma[5]
        g6 = self.gamma[6]
        g7 = self.gamma[7]
        g8 = self.gamma[8]

        a = matrix([[g1 * p * q - g2 * q * r],
                    [g5 * p * r - g6 * (pow(p, 2) - pow(r, 2))],
                    [g7 * p * q - g1 * q * r]])

        b = matrix([[g3 * l + g4 * n],
                    [m / self.jy],
                    [g4 * l + g8 * n]])
        # RETURNS Pdot Qdot Rdot
        pqrDot = a + b
        return pqrDot
