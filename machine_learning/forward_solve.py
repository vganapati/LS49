#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 13:30:54 2022

@author: vganapa1

Script creates a single image from a single simulated crystal with randomly chosen parameters
"""

import numpy as np
import matplotlib.pyplot as plt
from helper_functions import uniform_random_rotation
import sys


x = np.array([1,0,0])
x = np.expand_dims(x,axis=1)

all_rot = []
for i in range(10000):
    rot_x = uniform_random_rotation(x)
    all_rot.append(rot_x)

all_rot = np.concatenate(all_rot, axis=-1)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(all_rot[0], all_rot[1], all_rot[2], color = "green", s=0.01)
plt.show()

from LS49_pytorch.spectra.generate_spectra import spectra_simulation
SS = spectra_simulation()
print(SS)