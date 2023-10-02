import numpy as np 
import sys

sys.path.append('.')
import parameters.vtolParam as P

class vtolDynamics:
    def __init__(self, alpha=0.0):
        # Initial state conditions
        self.state = np.array([
            [P.z0],  # z initial position
            [P.h0],
            [P.theta0],  # Theta initial orientation
            [P.zdot0],  # zdot initial velocity
            [P.hdot0],
            [P.thetadot0],  # Thetadot initial velocity
        ])
        # simulation time step
        self.Ts = P.Ts
        # Physical parameters
        self.m = P.m
        self.J = P.J
        self.mr = P.mr
        self.ml = P.ml
        self.d = P.d
        self.mu = P.mu
        # gravity constant
        self.g = P.g
        self.force_limit = P.F_max

    def update(self, u):
        # This is the external method that takes the input u at time
        # t and returns the output y at time t.
        # saturate the input force
        u = saturate(u, self.force_limit)
        self.rk4_step(u)  # propagate the state by one time sample
        y = self.h()  # return the corresponding output
        return y

    def f(self, state, u):
        # Return xdot = f(x,u)
        z = state[0][0]
        h = state[1][0]
        theta = state[2][0]
        zdot = state[3][0]
        hdot = state[4][0]
        thetadot = state[5][0]
        fl = u[0][0]
        fr = u[1][0]
        # The equations of motion.
        M = np.array([[self.m+2*self.mr, 0, 0],
                      [0, self.m+2*self.mr, 0],
                      [0, 0, self.J+2*self.mr*self.d**2]])
        C = np.array([[-(fr+fl)*np.sin(theta)-self.mu*zdot],
                      [(fr+fl)*np.cos(theta)-(self.m+2*self.mr)*self.g],
                      [self.d*(fr-fl)]])
        tmp = np.linalg.inv(M) @ C # zddot thetddot
        zddot = tmp[0][0]
        hddot = tmp[1][0]
        thetaddot = tmp[2][0]
        # build xdot and return
        xdot = np.array([[zdot], [hdot], [thetadot], [zddot], [hddot], [thetaddot]])
        return xdot

    def h(self):
        # return y = h(x)
        z = self.state[0][0]
        h = self.state[1][0]
        theta = self.state[2][0]
        y = np.array([[z], [h], [theta]])
        return y

    def rk4_step(self, u):
        # Integrate ODE using Runge-Kutta RK4 algorithm
        F1 = self.f(self.state, u)
        F2 = self.f(self.state + self.Ts / 2 * F1, u)
        F3 = self.f(self.state + self.Ts / 2 * F2, u)
        F4 = self.f(self.state + self.Ts * F3, u)
        self.state += self.Ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)

        
def saturate(u, limit):
    shape = np.shape(u)
    u = u.flatten()
    for i in range(len(u)):
        if abs(u[i]) > limit:
            u[i] = limit*np.sign(u[i])
    u = np.reshape(u, shape)
    return u
