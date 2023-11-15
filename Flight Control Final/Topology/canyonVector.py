import numpy as np


class canyonVector:
    def __init__(self, dist=1, ang=15, n=100, offset=1/10, fac=1/2):
        self.array = np.zeros((n + 1, 2))
        self.a = np.copy(self.array)
        self.b = np.copy(self.array)
        self.dist = dist
        self.ang = np.deg2rad(ang)
        self.offset = dist * offset
        self.fac = offset * fac
        self.n = n
        self.create()
        self.ab = np.append(self.a, self.b, 1)

    def vector(self, point):
        length = np.random.rand() * self.dist
        angle = np.random.rand() * self.ang
        if np.random.rand() < .5:
            angle = -angle
        return np.array([length * np.sin(angle) + point[0], length * np.cos(angle) + point[1]])

    def noise(self, point):
        return np.array([point[0] + self.fac * np.random.rand(), point[1] + self.fac * np.random.rand()])

    def create(self):
        for i in range(self.n):
            self.array[i + 1] = self.vector(self.array[i])
            self.a[i + 1] = np.array(self.noise([self.array[i + 1, 0] + self.offset, self.array[i + 1, 1]]))
            self.b[i + 1] = np.array(self.noise([self.array[i + 1, 0] - self.offset, self.array[i + 1, 1]]))

    def store(self):
        np.savetxt('canyon.csv', self.ab, delimiter=',')
