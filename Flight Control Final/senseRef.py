import numpy as np
from Sensing import Sensing
import matplotlib.pyplot as plt
import matplotlib
import keyboard
matplotlib.use('TkAgg')

n = 4
temp = (-np.arange(n // 2) - 1) * np.pi / 2 / (n // 2)
sA = np.append(temp, np.abs(temp))

o = np.array([0, 0])
psi = np.pi / 2

b = np.array([[0, -1],
              [-1, 4],
              [-1.75, 8],
              [-2, 12],
              [-1, 16],
              [-1.5, 20]])
a = np.copy(b)
a[:, 0] += 3
a[0] = b[0]

t = 0
tf = 10000
ts = 0.1
v = .25
r = 8

lim = 25

s = Sensing(sA, o, psi, r, a, b)

fig = plt.figure()
ax = fig.add_subplot()

while t <= tf:
    if keyboard.is_pressed('up arrow'):
        o = o + np.array([np.cos(psi) * v, np.sin(psi) * v])
    if keyboard.is_pressed('right arrow'):
        psi -= 0.05
    if keyboard.is_pressed('left arrow'):
        psi += 0.05
    aInt, bInt, dA, dB = s.update(psi, o)

    ax.cla()
    ax.plot(a[:, 0], a[:, 1], color='black', marker='o')
    ax.plot(b[:, 0], b[:, 1], color='brown', marker='o')
    ax.plot(o[0], o[1], color='r', marker='o', markersize=5)
    ax.plot([o[0], r * np.cos(psi) + o[0]], [o[1], r * np.sin(psi) + o[1]], color='r', linestyle='--')

    plt.plot([o[0], aInt[0][0]], [o[1], aInt[0][1]],
             color='r', linestyle=':', label=f'{dA[0][0]:.2f}', alpha=.75)
    plt.plot([o[0], aInt[1][0]], [o[1], aInt[1][1]],
             color='b', linestyle='--', label=f'{dA[1][0]:.2f}', alpha=.5)
    plt.plot([o[0], bInt[0][0]], [o[1], bInt[0][1]],
             color='g', linestyle=':', label=f'{dB[0][0]:.2f}', alpha=.75)
    plt.plot([o[0], bInt[1][0]], [o[1], bInt[1][1]],
             color='c', linestyle='--', label=f'{dB[0][0]:.2f}', alpha=.5)

    ax.set_xlim(-lim / 2, lim / 2)
    ax.set_ylim(-1, lim - 1)
    ax.set_aspect('equal')
    ax.grid()
    ax.legend()
    plt.pause(ts)
    t += ts
