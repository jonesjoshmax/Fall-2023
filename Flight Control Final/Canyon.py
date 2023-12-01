import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection as p3d


class Canyon:
    def __init__(self, dist=1, ang=15, n=100, offset=1/4, fac=1/2, h=100):
        self.array = np.zeros((n + 1, 3))
        self.a = np.copy(self.array)
        self.b = np.copy(self.array)
        self.polyF = None
        self.polyC = None
        self.polyW = None
        self.polyA = None
        self.polyB = None
        self.aNorms = np.copy(self.array[:-1, :])
        self.bNorms = np.copy(self.array[:-1, :])
        self.dist = dist
        self.ang = np.deg2rad(ang)
        self.offset = dist * offset
        self.fac = offset * fac
        self.corner = self.offset * 50
        self.n = n
        self.h = h
        self.alpha = 1
        self.create()
        if self.a[1, 0] <= 0:
            self.a[1, 0] = np.abs(self.a[1, 0])
        if self.b[1, 0] >= 0:
            self.b[1, 0] = -self.b[1, 0]
        self.bounding()

    def vector(self, point):
        length = (np.random.rand() * 3) / 4 * self.dist
        angle = np.random.rand() * self.ang
        if np.random.rand() < .5:
            angle = -angle

        return np.array([length * np.sin(angle) + point[0], length * np.cos(angle) + point[1], 0])

    def noise(self, point):
        return np.array([point[0] + self.fac * np.random.rand(), point[1] + self.fac * np.random.rand(), 0])

    def create(self):
        for i in range(self.n):
            self.array[i + 1] = self.vector(self.array[i])
            self.a[i + 1] = np.array(self.noise([self.array[i + 1, 0] + self.offset, self.array[i + 1, 1], 0]))
            self.b[i + 1] = np.array(self.noise([self.array[i + 1, 0] - self.offset, self.array[i + 1, 1], 0]))

    def bounding(self):
        idx = np.tile(np.arange(0, self.n)[:, np.newaxis], 4)
        idx[:, 1:3] += 1
        verticesF = np.append(np.flip(self.b, 0)[:-1], self.a).reshape([self.n * 2 + 1, 3])
        verticesC = np.append(np.flip(self.b, 0)[:-1], self.a, 0)
        verticesC = np.append(verticesC, np.array([[self.corner, np.max(self.a), 0],
                                                   [self.corner, -self.corner, 0],
                                                   [-self.corner, -self.corner, 0],
                                                   [-self.corner, np.max(self.b), 0]]), 0)
        verticesC[:, 2] = np.ones(np.shape(verticesC)[0]) * self.h
        verticesW = np.array([[self.b[-1], [-self.corner, self.b[-1][1], 0], [-self.corner, self.b[-1][1], self.h],
                               self.b[-1] + np.array([0, 0, self.h])],
                              [self.a[-1], [self.corner, self.a[-1][1], 0], [self.corner, self.a[-1][1], self.h],
                               self.a[-1] + np.array([0, 0, self.h])]])
        verticesA = self.a[idx]
        verticesA[:, 2:, 2] += self.h
        verticesB = self.b[idx]
        verticesB[:, 2:, 2] += self.h
        c = np.array([175 / 255, 100 / 255, 75 / 255])
        color = c + (np.random.rand(self.n, 3) - 1) / 10
        self.polyF = p3d([verticesF], facecolors=c, alpha=self.alpha, zorder=0)
        self.polyC = p3d([verticesC], facecolors=np.array([255 / 255, 150 / 255, 100 / 255]), alpha=self.alpha, zorder=0)
        self.polyW = p3d(verticesW, facecolors=c, alpha=self.alpha, zorder=0)
        self.polyA = p3d(verticesA, facecolors=color, alpha=self.alpha, zorder=0)
        self.polyB = p3d(verticesB, facecolors=np.flip(color, 0), alpha=self.alpha, zorder=0)

