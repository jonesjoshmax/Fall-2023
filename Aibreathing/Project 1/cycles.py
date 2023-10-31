import numpy as np
import genEqns as e
from params import *


class Ideal:
    def __init__(self, bprIn=bpr, fprIn=pi_f, cprIn=pi_c):
        self.bpr = bprIn
        self.fpr = fprIn
        self.cpr = cprIn

    def calc(self):
        # COLD SECTION
        a0 = e.a(yc, R, Ta)
        v0 = a0 * M0

        to2 = Ta * e.tIse(yc, M0)
        po2 = Pa * e.pIse(yc, M0)

        to13 = to2 * e.tpIse(self.fpr, yc)
        po13 = po2 * self.fpr

        po13_a = po13 / Pa
        po19_c = e.pIse2(yc)
        chokeC = False
        if po13_a > po19_c:
            chokeC = True

        m19 = e.mpIse(po13_a, yc)
        to19 = to13
        t19 = to19 / e.tpIse(po13_a, yc)
        a19 = e.a(yc, R, t19)
        v19 = a19 * m19

        # HOT SECTION
        po3 = po13 * self.cpr
        to3 = to13 * e.tpIse(po3 / po13, yc)

        po4 = po3

        f = e.f(to3, to4, cpg, cpa, n_b, h_fuel)

        to4_to45 = (to3 - to13) * cpa / cpg
        to45_to5 = (self.bpr + 1) * (to13 - to2) * cpa / cpg
        to45 = to4 - to4_to45
        to5 = to45 - to45_to5
        po5 = po4 * e.ptIse(to5 / to4, yh)

        po9 = po5
        to9 = to5

        po9_pa = po9 / Pa
        po9_pe = e.pIse2(yh)
        chokeH = False
        if po9_pa > po9_pe:
            chokeH = True

        m9 = e.mpIse(po9_pa, yh)
        t9 = to9 / e.tpIse(po9_pa, yh)
        a9 = e.a(yh, R, t9)
        v9 = a9 * m9

        # RESULTING CALCS
        F = e.D(e.CD(cl), e.q(yc, Pa * 1e5, M0), S)
        mDot = e.mDot(F, v0, v19, v9, self.bpr)
        mDotC = mDot * (self.bpr / (self.bpr + 1))
        mDotH = mDot / (self.bpr + 1)
        rho = Pa * 1e5 / (R * Ta)
        A = mDot / (rho * v0)
        D = np.sqrt(4 * A / np.pi)
        mDotF = e.mDotFuel(mDotH, f)

        F_mDot = F / mDot
        tsfc = e.tsfc(mDotF, F) * 3600
        n_p = e.nP(v0, v19, v9, mDot, mDotC, mDotH)
        n_t = e.nT(v0, v19, v9, mDot, mDotC, mDotH, mDotF, h_fuel)
        n_o = n_p * n_t

        out = np.array([F_mDot, tsfc, f, n_t, n_p, n_o]).T
        return out


class Real:
    def __init__(self, bprIn=bpr, fprIn=pi_f, cprIn=pi_c):
        self.bpr = bprIn
        self.fpr = fprIn
        self.cpr = cprIn

    def calc(self):
        # EFFICIENCIES
        nFan = (yc - 1) / (yc * n_if)
        nComp = (yc - 1) / (yc * n_ic)
        nTurb = n_it * (yh - 1) / yh

        # SECTION
        to2 = Ta * e.tIse(yc, M0)
        po2 = Pa * e.pIseR(yc, M0, n_i)

        to13 = to2 * self.fpr ** nFan
        po13 = po2 * self.fpr
        to3 = to13 * self.cpr ** nComp
        po3 = po13 * self.cpr

        po4 = po3 * pi_b

        f = e.f(to3, to4, cpg, cpa, n_b, h_fuel)
        mDotTot_mDotH = e.mDotRatio(f, self.bpr)

        to4_to5 = e.delT(to2, to13, to3, cpa, cpg, n_m, f, mDotTot_mDotH)
        to5 = to4 - to4_to5
        po5 = po4 * e.ptIseR(to5 / to4, nTurb)

        to6 = to5
        po6 = po5

        po9 = po6

        po9_pa = po9 / Pa
        po9_pc = e.pIse2(yh)
        chokeH = False
        if po9_pa > po9_pc:
            chokeH = True

        to9 = e.tDelT(to6, Pa / po9, n_j, yh)

        m9 = e.mpIse(po9_pa, yc)
        a9 = e.a(yc, R, to9)
        v9 = a9 * m9

        # COLD SECTION
        a0 = e.a(yc, R, Ta)
        v0 = a0 * M0

        po13_pa = po13 / Pa
        po13_pc = 1 / e.pIseR2(yc, n_m)
        chokeC = False
        if po13_pa > po13_pc:
            chokeC = True

        m19 = e.mpIse(po13 / Pa, yc)
        t19 = e.tDelT(to13, Pa / po13, n_j, yc)
        a19 = e.a(yc, R, t19)
        v19 = m19 * a19

        # RESULTING CALCS
        F = e.D(e.CD(cl), e.q(yc, Pa * 1e5, M0), S)
        mDot = e.mDotR(F, f, v0, v19, v9, self.bpr)
        mDotC = mDot * (self.bpr / (self.bpr + 1))
        mDotH = mDot * ((1 - f) / (self.bpr + 1))
        rho = Pa * 1e5 / (R * Ta)
        A = mDot / (rho * v0)
        D = np.sqrt(4 * A / np.pi)
        mDotF = e.mDotFuel(mDotH, f)

        F_mDot = F / mDot
        tsfc = e.tsfc(mDotF, F) * 3600
        n_p = e.nP(v0, v19, v9, mDot, mDotC, mDotH)
        n_t = e.nT(v0, v19, v9, mDot, mDotC, mDotH, mDotF, h_fuel)
        n_o = n_p * n_t

        out = np.array([F_mDot, tsfc, f, n_t, n_p, n_o]).T
        return out
