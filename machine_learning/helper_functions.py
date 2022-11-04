#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 14:08:10 2022

@author: vganapa1

Reference: https://www.blopig.com/blog/2021/08/uniformly-sampled-3d-rotation-matrices/
"""

import numpy as np

def generate_random_z_axis_rotation():
    """Generate random rotation matrix about the z axis."""
    R = np.eye(3)
    x1 = np.random.rand()
    R[0, 0] = R[1, 1] = np.cos(2 * np.pi * x1)
    R[0, 1] = -np.sin(2 * np.pi * x1)
    R[1, 0] = np.sin(2 * np.pi * x1)
    return(R)

def uniform_random_rotation(x):
    """Apply a random rotation in 3D, with a distribution uniform over the
    sphere.

    Arguments:
        x: vector of shape (3,1)
    Returns:
        Vector of shape (3,1) containing the randomly rotated vectors of x (all have the same rotation)

    Algorithm taken from "Fast Random Rotation Matrices" (James Avro, 1992):
    https://doi.org/10.1016/B978-0-08-050755-2.50034-8
    """

    # There are two random variables in [0, 1) here (naming is same as paper)
    x2 = 2 * np.pi * np.random.rand()
    x3 = np.random.rand()

    # Rotation of all points around z axis using matrix
    R = generate_random_z_axis_rotation()
    
    # Rotate the z axis to a random point on unit sphere
    v = np.array([
        np.cos(x2) * np.sqrt(x3),
        np.sin(x2) * np.sqrt(x3),
        np.sqrt(1 - x3)
    ])
    H = np.eye(3) - (2 * np.outer(v, v))
    
    # total rotation matrix
    M = -(H @ R)

    print(M.shape)
    
    return(M@x)