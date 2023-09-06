from matplotlib import pyplot as plt
from matplotlib import patches as mpatches
import numpy as np
import A1P2Parameters as p


class Visualizer:
    def __init__(self):
        self.flag_init = True
        self.fig, self.ax = plt.subplots()
        self.handle = []
        plt.pause(15)
        plt.plot([0.0, p.l], [0.0, 0.0], 'black')
        plt.axis([0, p.l + p.l / 5, 0, p.l + p.l / 5])

    def update(self, state, forces, cart=0.0):
        z = state[0][0]  # Horizontal position of cart, m
        h = state[1][0]  # Vertical position of cart, m
        theta = state[2][0]  # Angle of vtol, rads
        ul = forces[0]
        ur = forces[1]
        # draw plot, vtol, cart
        self.vehicle(z, h, theta)
        self.cart(cart)
        self.ax.axis('equal')
        # Set initialization flag to False after first call
        if self.flag_init:
            self.flag_init = False

    def vehicle(self, z, h, th):
        x1 = p.w
        x2 = p.gap
        x3 = p.gap + p.w
        y1 = p.h
        y2 = p.h2
        pts = np.array([[x1, y1],
                        [x1, 0],
                        [x2, 0],
                        [x2, y2],
                        [x3, y2],
                        [x3, -y2],
                        [x2, -y2],
                        [x2, 0],
                        [x1, 0],
                        [x1, -y1],
                        [-x1, -y1],
                        [-x1, 0],
                        [-x2, 0],
                        [-x2, -y2],
                        [-x3, -y2],
                        [-x3, y2],
                        [-x2, y2],
                        [-x2, 0],
                        [-x1, 0],
                        [-x1, y1],
                        [x1, y1]]).T
        R = np.array([
            [np.cos(th), np.sin(th)],
            [-np.sin(th), np.cos(th)]
        ])
        pts = R.T @ pts
        pts = pts + np.tile(np.array([[z], [h]]), (1, pts.shape[1]))
        xy = np.array(pts.T)

        if self.flag_init:
            self.handle.append(mpatches.Polygon(xy, facecolor='r', edgecolor='black'))
            self.ax.add_patch(self.handle[0])
        else:
            self.handle[0].set_xy(xy)

    def cart(self, cart=0.0):
        w = p.w
        h = p.h
        pts = np.matrix([
            [cart + w / 2.0, h],
            [cart + w / 2.0, 0],
            [cart - w / 2.0, 0],
            [cart - w / 2.0, h],
            [cart + w / 2.0, h]
        ])
        # INITIALIZATION FLAG POINT
        if self.flag_init:
            self.handle.append(mpatches.Polygon(pts, facecolor='red', edgecolor='black'))
            self.ax.add_patch(self.handle[1])
        else:
            self.handle[1].set_xy(pts)
