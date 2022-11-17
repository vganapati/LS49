#!/bin/bash -l
#SBATCH -N 1             # Number of nodes
#SBATCH -J kokkos_migration
#SBATCH -A m3562_g       # allocation
#SBATCH -C gpu
#SBATCH -q regular # regular or special queue
#SBATCH -t 00:05:00      # wall clock time limit
#SBATCH --gpus-per-node 1
#SBATCH -o job%j.out
#SBATCH -e job%j.err

export WORK=$WORK/adse13_249/LY99
export CCTBX_DEVICE_PER_NODE=1
export N_START=0
cd $WORK

export LOG_BY_RANK=1 # Use Aaron's rank logger
export RANK_PROFILE=0 # 0 or 1 Use cProfiler, default 1
export N_SIM=1 # total number of images to simulate
export ADD_BACKGROUND_ALGORITHM=cuda # cuda or jh or sort_stable
export DEVICES_PER_NODE=1
export MOS_DOM=25

export CUDA_LAUNCH_BLOCKING=1

mkdir $SLURM_JOB_ID; cd $SLURM_JOB_ID
echo "jobstart $(date)";pwd
srun -n 32 -c 2 libtbx.python $MODULES/LS49/adse13_196/revapi/LY99_batch.py noise=True psf=False attenuation=True context=kokkos_gpu
echo "jobend $(date)";pwd
