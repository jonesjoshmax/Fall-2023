import numpy as np


class Sensing:
    def __init__(self, sensors, origin, psi, radius, boundA, boundB):
        # SENSORS INPUT: [[ANGLE_1], [ANGLE_2], [ANGLE_N]]
        self.s = sensors
        self.n = np.size(sensors)
        self.dA = np.zeros((self.n // 2, 1))
        self.dB = np.zeros((self.n // 2, 1))
        self.sA = np.zeros((np.size(sensors), 1))
        self.cA = np.zeros((np.size(sensors), 2))
        self.r = radius
        self.o = origin
        self.a = boundA
        self.b = boundB
        self.psi = psi

        self.xS = self.o[0] + self.r * np.cos(self.psi + self.s)
        self.yS = self.o[1] + self.r * np.sin(self.psi + self.s)
        self.aOld = np.zeros([self.n // 2, 2])
        self.bOld = np.zeros([self.n // 2, 2])
        self.aA = None
        self.aB = None
        self.ang = None
        self.idx = None
        self.aVec = None
        self.bVec = None
        self.aLine = None
        self.bLine = None
        self.aInter = None
        self.bInter = None

    def update(self, psi, o):
        # UPDATING VARIABLES
        self.o = o
        self.psi = psi
        # CALCULATING RELEVANT ANGLES
        self.aA = np.arctan2(self.a[:, 1] - self.o[1], self.a[:, 0] - self.o[0]) + np.pi
        self.aB = np.arctan2(self.b[:, 1] - self.o[1], self.b[:, 0] - self.o[0]) + np.pi
        # CORRECT ANGLES TO 0 <= ANG <= 2 * PI
        self.aA[np.where(self.aA > 2 * np.pi)] -= 2 * np.pi
        self.aB[np.where(self.aB > 2 * np.pi)] -= 2 * np.pi
        # LOCATIONS OF SENSOR TARGET POINTS
        self.xS = self.o[0] + self.r * np.cos(self.psi + self.s.reshape(np.size(self.s), 1))
        self.yS = self.o[1] + self.r * np.sin(self.psi + self.s.reshape(np.size(self.s), 1))
        self.sA = np.append(self.xS, self.yS, 1)
        # CORRECTED VALUES OF ANGLES
        self.ang = self.npBound(self.psi + self.s)
        # FINDING CLOSEST ANGLED POINTS INDEXED ONE BACK WHEN CANYON ANGLE IS GREATER
        idx = self.near(self.a, self.b, self.o, self.s, self.psi, self.r, self.n)
        # INTERSECTION POINT MATH
        xTile = np.tile(self.o[0], (self.n // 2, 1))
        yTile = np.tile(self.o[1], (self.n // 2, 1))
        self.aVec = np.append(xTile, self.xS[:self.n // 2], 1)
        self.aVec = np.append(self.aVec, yTile, 1)
        self.aVec = np.append(self.aVec, self.yS[:self.n // 2], 1)
        self.bVec = np.append(xTile, self.xS[self.n // 2:], 1)
        self.bVec = np.append(self.bVec, yTile, 1)
        self.bVec = np.append(self.bVec, self.yS[self.n // 2:], 1)
        self.aLine = np.append(self.a[idx[0]][:, 0].reshape(np.shape(idx)[1], 1),
                               self.a[(idx + 1)[0]][:, 0].reshape(np.shape(idx)[1], 1), 1)
        self.aLine = np.append(self.aLine, self.a[idx[0]][:, 1].reshape(np.shape(idx)[1], 1), 1)
        self.aLine = np.append(self.aLine, self.a[(idx + 1)[0]][:, 1].reshape(np.shape(idx)[1], 1), 1)
        self.bLine = np.append(self.b[idx[1]][:, 0].reshape(np.shape(idx)[1], 1),
                               self.b[(idx + 1)[1]][:, 0].reshape(np.shape(idx)[1], 1), 1)
        self.bLine = np.append(self.bLine, self.b[idx[1]][:, 1].reshape(np.shape(idx)[1], 1), 1)
        self.bLine = np.append(self.bLine, self.b[(idx + 1)[1]][:, 1].reshape(np.shape(idx)[1], 1), 1)
        self.aOld = self.intersection(self.aVec, self.aLine, self.aOld)
        self.bOld = self.intersection(self.bVec, self.bLine, self.bOld)
        self.dA = np.sqrt((self.aOld[:, 0].reshape(np.size(xTile), 1) - xTile) ** 2 +
                          (self.aOld[:, 1].reshape(np.size(yTile), 1) - yTile) ** 2)
        self.dB = np.sqrt((self.bOld[:, 0].reshape(np.size(xTile), 1) - xTile) ** 2 +
                          (self.bOld[:, 1].reshape(np.size(yTile), 1) - yTile) ** 2)

        return self.aOld, self.bOld, self.dA, self.dB

    @staticmethod
    def npBound(arr):
        arr[np.where(arr < 0)] = arr[np.where(arr < 0)] + 2 * np.pi
        arr[np.where(arr >= 2 * np.pi)] = arr[np.where(arr >= 2 * np.pi)] - 2 * np.pi
        return arr

    @staticmethod
    def near(a, b, o, s, psi, r, n):
        senA = np.abs((s + psi)[:n // 2] - np.pi / 2)
        senB = (s + psi)[n // 2:] - np.pi / 2
        angA = np.abs(np.arctan2(a[:, 1] - o[1], a[:, 0] - o[0]) - np.pi / 2)
        angB = np.abs(-np.arctan2(o[1] - b[:, 1], o[0] - b[:, 0]) - np.pi / 2)
        idxA = np.array(np.where(np.sqrt((a[:, 0] - o[0]) ** 2 + (a[:, 1] - o[1]) ** 2) <= r))[0]
        idxB = np.array(np.where(np.sqrt((b[:, 0] - o[0]) ** 2 + (b[:, 1] - o[1]) ** 2) <= r))[0]
        difA = np.abs(angA[idxA].reshape(np.size(idxA), 1) - senA)
        minA = difA.argmin(axis=0)
        minA[np.where(angA[idxA][minA] < senA)] -= 1

        difB = np.abs(angB[idxB].reshape(np.size(idxB), 1) - senB)
        minB = difB.argmin(axis=0)
        minB[np.where(angB[idxB][minB] < senB)] -= 1
        idx = np.array([idxA[minA], idxB[minB]])
        return idx

    @staticmethod
    def intersection(vec, lin, old):
        d = (lin[:, 3] - lin[:, 2]) * (vec[:, 1] - vec[:, 0]) - \
            (vec[:, 3] - vec[:, 2]) * (lin[:, 1] - lin[:, 0])
        t = ((lin[:, 1] - lin[:, 0]) * (vec[:, 2] - lin[:, 2]) -
             (lin[:, 3] - lin[:, 2]) * (vec[:, 0] - lin[:, 0])) / d
        s = ((vec[:, 1] - vec[:, 0]) * (vec[:, 2] - lin[:, 2]) -
             (vec[:, 3] - vec[:, 2]) * (vec[:, 0] - lin[:, 0])) / d
        logic = np.where(((np.zeros(np.size(t)) <= t) & (t <= np.ones(np.size(t)))
                          & (np.zeros(np.size(t)) <= s) & (s <= np.ones(np.size(t)))))
        xInt = vec[logic, 0][0].reshape(np.size(logic), 1) + t[logic].reshape(np.size(logic), 1)[:] * \
               (vec[logic, 1][0].reshape(np.size(logic), 1) - vec[logic, 0][0].reshape(np.size(logic), 1))
        yInt = vec[logic, 2][0].reshape(np.size(logic), 1) + t[logic].reshape(np.size(logic), 1)[:] * \
               (vec[logic, 3][0].reshape(np.size(logic), 1) - vec[logic, 2][0].reshape(np.size(logic), 1))
        inter = np.append(xInt, yInt, 1)
        fill = np.where(((np.zeros(np.size(t)) > t) | (np.ones(np.size(t)) < t)
                          | (np.zeros(np.size(t)) > s) | (np.ones(np.size(t)) < s)))
        if 1 >= np.size(fill) > 0:
            inter = np.insert(inter, fill[0][0], old[fill[0][0]], axis=0)
        elif np.size(fill) > 1:
            inter = old
        return inter
