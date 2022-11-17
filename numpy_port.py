#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 13:30:07 2022

@author: vganapa1
"""

'''
Forward solution workflow with cctbx:

Open Perlmutter terminal

source ~/env_p20231

cd $WORK/adse13_249/LY99
export CCTBX_DEVICE_PER_NODE=1
export N_START=0

export LOG_BY_RANK=1 # Use Aaron's rank logger
export RANK_PROFILE=0 # 0 or 1 Use cProfiler, default 1
export N_SIM=1 # total number of images to simulate
export ADD_BACKGROUND_ALGORITHM=cuda # cuda or jh or sort_stable
export DEVICES_PER_NODE=1
export MOS_DOM=25
export CUDA_LAUNCH_BLOCKING=1

libtbx.python $MODULES/LS49/adse13_196/revapi/LY99_batch.py noise=True psf=False attenuation=True context=kokkos_gpu
dials.image_viewer XXX.img.gz

 it worked!!!

'''