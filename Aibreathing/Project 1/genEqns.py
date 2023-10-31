import numpy as np


def a(y, R, T):
    return np.sqrt(y * R * T)


def v(a, M):
    return a * M


def q(y, P, M):
    return y * P * M ** 2 / 2


def L(CL, q, S):
    return CL * q * S


def CD(CL):
    return 0.056 * CL ** 2 - 0.004 * CL + 0.0140


def D(CD, q, S):
    return CD * q * S


def tIse(y, M):
    return 1 + (y - 1) * M ** 2 / 2


def pIse(y, M):
    return (1 + (y - 1) * M ** 2 / 2) ** (y / (y - 1))


def pIseR(y, M, n):
    return (1 + (y - 1) * M ** 2 / (2 * n)) ** (y / (y - 1))


def pIse2(y):
    return (1 + (y - 1) / 2) ** (y / (y - 1))


def pIseR2(y, n):
    return (1 - (y - 1) / ((y + 1) * n)) ** (y / (y - 1))


def tpIse(pr, y):
    return pr ** ((y - 1) / y)


def ptIse(tr, y):
    return tr ** (y / (y - 1))


def ptIseR(tr, n):
    return tr ** (1 / n)


def mpIse(pr, y):
    return (np.sqrt(2) * np.sqrt(pr ** ((y - 1) / y) - 1)) / np.sqrt(y - 1)


def mDot(F, va, vc, vh, bpr):
    return F / (bpr / (bpr + 1) * (vc - va) + (vh - va) / (bpr + 1))


def mDotR(F, f, va, vc, vh, bpr):
    return F / (bpr / (bpr + 1) * (vc - va) + (vh - va) * (1 - f) / (bpr + 1))


def mDotRatio(f, r):
    return 1 + f + r


def delT(ta, t1b, tb, cpa, cpg, nm, f, mDR):
    return (cpa * (tb - t1b) + mDR * cpa * (t1b - ta)) / (nm * cpg * (1 + f))


def tDelT(t, pr, nj, y):
    return t - nj * t * (1 - pr ** ((y - 1) / y))


def f(ta, tb, cpg, cpa, nb, h):
    return (cpg * tb - cpa * ta) / (nb * (h - cpg * tb))


def mDotFuel(m0, f):
    return m0 * f


def tsfc(mDotFuel, F):
    return mDotFuel / F


def nT(c0, c19, c9, m0, mc, mh, mf, h):
    return ((mh * (c9 ** 2) + mc * (c19 ** 2) - m0 * (c0 ** 2)) / 2) / (mf * h) / 1000


def nP(c0, c19, c9, m0, mc, mh):
    return (c0 * (mc * (c19 - c0) + mh * (c9 - c0))) / ((mh * c9 ** 2 + mc * c19 ** 2 - m0 * c0 ** 2) / 2)
