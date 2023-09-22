import numpy as np
import control
from control.matlab import *


def Body2Inertial(phi, theta, psi):
    rbw = np.array([[np.cos(theta) * np.cos(psi),
                     np.sin(phi) * np.sin(theta) * np.cos(psi) - np.cos(phi) * np.sin(psi),
                     np.cos(phi) * np.sin(theta) * np.cos(psi)
                     + np.sin(phi) * np.sin(psi)],
                    [np.cos(theta) * np.sin(psi),
                     np.sin(phi) * np.sin(theta) * np.sin(psi) + np.cos(phi) * np.cos(psi),
                     np.cos(phi) * np.sin(theta) * np.sin(psi)
                     - np.sin(phi) * np.cos(psi)],
                    [-np.sin(theta), np.sin(phi) * np.cos(theta), np.cos(phi) * np.cos(theta)]])
    return rbw


def wind(phi, theta, psi, Va, dt):
    # STEADY WIND INERTIAL FRAME
    wn = 5
    we = 3
    wd = 2

    # GUST PARAMS
    Lu = 200
    Lv = 200
    Lw = 50
    sigma_u = 1.06  # 2.12
    sigma_v = sigma_u
    sigma_w = 0.7  # 1.4
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

    # SIMULATION RAND
    T = [0, dt]
    X0 = 0.0
    white_noise_u = np.random.normal(0, 1, 1)
    white_noise_v = np.random.normal(0, 1, 1)
    white_noise_w = np.random.normal(0, 1, 1)
    y_u, T, x_u = lsim(sys_u, white_noise_u[0], T, X0)
    y_v, T, x_v = lsim(sys_v, white_noise_v[0], T, X0)
    y_w, T, x_w = lsim(sys_w, white_noise_w[0], T, X0)

    # GUST COMPONENTS
    wg_u = y_u[1]
    wg_v = y_v[1]
    wg_w = y_w[1]
    Ws_v = np.array([wn, we, wd])  # WIND IN VEHICLE
    R = Body2Inertial(phi, theta, psi)  # V2B ROTATION MATRIX
    Ws_b = np.matmul(R.T, Ws_v.T).T  # WIND IN BODY
    Wg_b = np.array([wg_u, wg_v, wg_w])
    Vw = Wg_b + Ws_b

    return Vw
