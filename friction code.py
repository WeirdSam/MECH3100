# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 13:38:06 2022

@author: User
"""
import numpy as np
from matplotlib import pyplot as plt 

w_i = 10 #kg
w_f_max = 69.5 #kg

mu_s_sled = 0.58 #static coefficient of friction used

mu_chock = 0.86 #rubber

w_t = 52 #kg
dist = 7 #m
inc_dist = 5 #m

W = np.linspace(w_i, w_f_max, 100)
Ff = W * mu_s_sled
D_1 = np.linspace(0, inc_dist, 100)
W_s = np.ones(40) * w_f_max
Ff_s = W_s * mu_s_sled
D_2 = np.linspace(inc_dist, dist, 40)

D = np.linspace(0, dist, 140)
T = np.ones(140) * mu_chock * w_t

fig, ax = plt.subplots()
ax.set_ylabel('friction forces (N)')
ax.set_xlabel('Distance (m)')
fig.suptitle('friction of sled and traction of tractor')

ax.plot(D_1, Ff, 'b', label = 'Sled Frcition')
ax.plot(D_2, Ff_s, 'b')
ax.plot(D, T, 'r', label = 'Tractor Traction')
plt.legend()
ax.grid()
plt.show()