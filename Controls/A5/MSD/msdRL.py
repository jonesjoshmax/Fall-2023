import control as c
from msdParameters import *

tf = c.tf([1], [m, b + kd, k + kp, 0])
c.rlocus(tf)
