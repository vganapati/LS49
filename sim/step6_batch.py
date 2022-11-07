from __future__ import division, print_function
from six.moves import range
from scitbx.matrix import sqr
from time import time
from omptbx import omp_get_num_procs

# %%% boilerplate specialize to packaged big data %%%
from LS49.sim import step6_pad
from LS49.sim import step5_pad
from LS49.sim import step4_pad
from LS49.spectra import generate_spectra
from LS49 import ls49_big_data
step6_pad.big_data = ls49_big_data
step5_pad.big_data = ls49_big_data
step4_pad.big_data = ls49_big_data
generate_spectra.big_data = ls49_big_data
# %%%%%%

# Develop procedure for MPI control

def tst_one(image,spectra,crystal,random_orientation):
  iterator = spectra.generate_recast_renormalized_image(image=image,energy=7120.,total_flux=1e12)

  quick = False
  if quick: prefix_root="step6_batch_%06d"
  else: prefix_root="step6_MPIbatch_%06d"

  file_prefix = prefix_root%image
  rand_ori = sqr(random_orientation)
  from LS49.sim.step6_pad import run_sim2smv
  run_sim2smv(prefix = file_prefix,crystal = crystal,spectra=iterator,rotation=rand_ori,quick=quick,rank=rank)

if __name__=="__main__":
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  size = comm.Get_size()
  N_total = 1 # number of items to simulate
  N_stride = size # total number of worker tasks
  print("hello from rank %d of %d"%(rank,size),"with omp_threads=",omp_get_num_procs())
  if rank == 0:
    from LS49.spectra.generate_spectra import spectra_simulation
    from LS49.sim.step6_pad import microcrystal
    print("hello2 from rank %d of %d"%(rank,size))
    SS = spectra_simulation()
    C = microcrystal(Deff_A = 4000, length_um = 4., beam_diameter_um = 1.0) # assume smaller than 10 um crystals
    from LS49 import legacy_random_orientations
    random_orientations = legacy_random_orientations(N_total)
    transmitted_info = dict(spectra = SS,
                            crystal = C,
                            random_orientations = random_orientations)
  else:
    transmitted_info = None
  transmitted_info = comm.bcast(transmitted_info, root = 0)
  comm.barrier()
  parcels = list(range(rank,N_total,N_stride))
  while len(parcels)>0:
    import random
    idx = random.choice(parcels)
    print("idx------start-------->",idx,"rank",rank,time())
    tst_one(image=idx,spectra=transmitted_info["spectra"],
            crystal=transmitted_info["crystal"],random_orientation=transmitted_info["random_orientations"][idx])
    parcels.remove(idx)
    print("idx------finis-------->",idx,"rank",rank,time())
  print("OK exiting rank",rank)
