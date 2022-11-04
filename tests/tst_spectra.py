#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 14:38:19 2022

@author: vganapa1
"""

from LS49_pytorch.spectra.generate_spectra import spectra_simulation
SS = spectra_simulation()
print(SS)
print(SS.N)
print(SS.R["spectra"][0])
print(SS.R["spectra"])