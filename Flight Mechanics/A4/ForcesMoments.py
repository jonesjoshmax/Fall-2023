import numpy as np
from Parameters import *
from Rotations import Euler2Rotation
from math import cos, sin
from control.matlab import *
from MAV import MAV

mav = MAV()


class ForcesMoments:
    def __init__(self):
        self.temp = None

    def compute(self, state, data):
        pn, pe, pd, u, v, w, ph, th, ps, p, q, r = state.flatten()
        De, Da, Dr, Dt = data.flatten()

        Va, alpha, beta = self.air_data(state)
        q_ = 0.5 * rho * Va ** 2
        ca = cos(alpha)
        sa = sin(alpha)

        # GRAVITATIONAL FORCES
        fx = -mass * g * sin(th)
        fy = mass * g * cos(th) * sin(ph)
        fz = mass * g * cos(th) * cos(ph)

        # LIFT AND DRAG
        tmp1 = np.exp(-M * (alpha - alpha0))
        tmp2 = np.exp(M * (alpha + alpha0))
        sigma = (1 + tmp1 + tmp2) / ((1 + tmp1) * (1 + tmp2))
        cl = (1 - sigma) * (cl0 + cla * alpha)

        cd = cd0 + 1 / (np.pi * e * AR) * (cl0 + cla * alpha) ** 2
        cl = cl + np.sign(alpha) * sigma * 2 * sa * sa * ca

        # AERO FORCES
        fx = fx + q_ * S * (-cd * ca + cl * sa)
        fx = fx + q_ * S * (-cdq * ca + clq * sa) * c * q / (2 * Va)

        fy = fy + q_ * S * (cY0 + cYb * beta)
        fy = fy + q_ * S * (cYp * p + cYr * r) * b / (2 * Va)

        fz = fz + q_ * S * (-cd * sa - cl * ca)
        fz = fz + q_ * S * (-cdq * sa - clq * ca) * c * q / (2 * Va)

        # AERO MOMENTS
        phM = q_ * S * b * (cL0 + cLb * beta)
        phM = phM + q_ * S * b * (cLp * p + cLr * r) * b / (2 * Va)

        thM = q_ * S * c * (cm0 + cma * alpha)
        thM = thM + q_ * S * c * cmq * c * q / (2 * Va)

        psM = q_ * S * b * (cN0 + cNb * beta)
        psM = psM + q_ * S * b * (cNp * p + cNr * r) * b / (2 * Va)

        # CONTROL FORCES
        fx = fx + q_ * S * (-cdDe * ca + clDe * sa) * De
        fy = fy + q_ * S * (cYDa * Da + cYDr * Dr)
        fz = fz + q_ * S * (-cdDe * sa - clDe * ca) * De

        # CONTROL MOMENTS
        phM = phM + q_ * S * b * (cLDa * Da + cLDr * Dr)
        thM = thM + q_ * S * c * cmDe * De
        psM = psM + q_ * S * b * (cNDa * Da + cNDr * Dr)

        # PROPULSION FORCE
        fProp = kMotor ** 2 * Dt ** 2 - Va ** 2
        fx = fx + 0.5 * rho * S_prop * cProp * fProp

        return np.array([[fx], [fy], [fz]], dtype=float), np.array([[phM], [thM], [psM]], dtype=float)

    @staticmethod
    def wind(phi, theta, psi, Va, dt):
        # STEADY WIND
        wn = 0.
        we = 0.
        wd = 0.

        # GUST PARAMETERS
        Lu = 200
        Lv = 200
        Lw = 50
        sigma_u = 1.06
        sigma_v = sigma_u
        sigma_w = 0.7

        au = sigma_u * np.sqrt(2 * Va / Lu)
        av = sigma_v * np.sqrt(3 * Va / Lv)
        aw = sigma_w * np.sqrt(3 * Va / Lw)

        # TRANSFER FUNCTIONS
        num_u = [0, au]
        den_u = [1, Va / Lu]
        sys_u = tf(num_u, den_u)

        num_v = [av, av * Va / (np.sqrt(3) * Lv)]
        den_v = [1, 2 * Va / Lv, (Va / Lv) ** 2]
        sys_v = tf(num_v, den_v)

        num_w = [aw, aw * Va / (np.sqrt(3) * Lw)]
        den_w = [1, 2 * Va / Lw, (Va / Lw) ** 2]
        sys_w = tf(num_w, den_w)

        T = [0, dt]
        X0 = 0.0
        white_noise_u = np.random.normal(0, 1, 1)
        white_noise_v = np.random.normal(0, 1, 1)
        white_noise_w = np.random.normal(0, 1, 1)

        y_u, T, x_u = lsim(sys_u, white_noise_u[0], T, X0)
        y_v, T, x_v = lsim(sys_v, white_noise_v[0], T, X0)
        y_w, T, x_w = lsim(sys_w, white_noise_w[0], T, X0)

        # GUST COMPONENT
        Ws_v = np.array([wn, we, wd])
        R = Euler2Rotation(phi, theta, psi)
        Ws_b = np.matmul(R.T, Ws_v.T).T

        return Ws_b

    @staticmethod
    def air_data(state):
        # STEADY STATE WIND
        pn, pe, pd, u, v, w, ph, th, ps, p, q, r = state.flatten()
        Va = np.sqrt(u ** 2 + v ** 2 + w ** 2)
        alpha = np.arctan2(w, u)
        beta = np.arctan2(v, Va)

        return Va, alpha, beta
