#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 15:09:59 2022

@author: vganapa1
"""

from __future__ import division, print_function
from time import time
start_elapse = time()

from six.moves import range
from scitbx.matrix import sqr
from scitbx.array_family import flex

# %%% boilerplate specialize to packaged big data %%%
from LS49.adse13_196.revapi import LY99_pad
from LS49.sim import step4_pad
from LS49.spectra import generate_spectra
from LS49 import ls49_big_data
LY99_pad.big_data = ls49_big_data
step4_pad.big_data = ls49_big_data
generate_spectra.big_data = ls49_big_data
from LS49.sim.util_fmodel import gen_fmodel
from LS49.adse13_196.revapi.LY99_pad import data


def parse_input():
  from iotbx.phil import parse
  master_phil="""
    logger {
      outdir = .
        .type = path
        .help = Use "/mnt/bb/${USER}" for Summit NVME burst buffer
    }
    context = kokkos_gpu kokkos_cpu *cuda
      .type = choice
      .help = backend for parallel execution
      .help = Note, for now the assumption that default==cuda is baked in to the tests
      .help = specifically tst_step5_batch_single_process_GPU.py
    noise = True
      .type = bool
    psf = True
      .type = bool
    attenuation = True
      .type = bool
  """
  phil_scope = parse(master_phil)
  # The script usage
  help_message = '''ADSE13-196.'''
  usage = ""
  '''Initialize the script.'''
  from dials.util.options import ArgumentParser
  # Create the parser
  parser = ArgumentParser(
        usage=usage,
        phil=phil_scope,
        epilog=help_message)

  # Parse the command line. quick_parse is required for MPI compatibility
  params, options = parser.parse_args(show_diff_phil=True,quick_parse=True)
  return params,options

def tst_one(image,spectra,crystal,random_orientation,sfall_channels,params):

  iterator = spectra.generate_recast_renormalized_image(image=image%100000,energy=7120.,total_flux=1e12)

  quick = True
  if quick: prefix_root="LY99_batch_%06d"
  else: prefix_root="LY99_MPIbatch_%06d"

  file_prefix = prefix_root%image
  rand_ori = sqr(random_orientation)
  from LS49_pytorch.adse13_196.revapi.LY99_pad import run_sim2smv
  run_sim2smv(prefix = file_prefix,
              crystal = crystal,
              spectra=iterator,rotation=rand_ori,
              sfall_channels=sfall_channels,params=params)

def run_LY99_batch(test_without_mpi=False):
  params,options = parse_input()
  print(params)

  N_total = 1

  # now inside the Python imports, begin energy channel calculation

  wavelength_A = 1.74 # general ballpark X-ray wavelength in Angstroms
  wavlen = flex.double([12398.425/(7070.5 + w) for w in range(100)])
  direct_algo_res_limit = 1.7

  local_data = data() # later put this through broadcast

  GF = gen_fmodel(resolution=direct_algo_res_limit,
                  pdb_text=local_data.get("pdb_lines"),algorithm="fft",wavelength=wavelength_A)
  GF.set_k_sol(0.435)
  GF.make_P1_primitive()

  # Generating sf for my wavelengths
  sfall_channels = {}
  for x in range(len(wavlen)):

    GF.reset_wavelength(wavlen[x])
    GF.reset_specific_at_wavelength(
                     label_has="FE1",tables=local_data.get("Fe_oxidized_model"),newvalue=wavlen[x])
    GF.reset_specific_at_wavelength(
                     label_has="FE2",tables=local_data.get("Fe_reduced_model"),newvalue=wavlen[x])
    sfall_channels[x]=GF.get_amplitudes()



  from LS49.spectra.generate_spectra import spectra_simulation
  from LS49.adse13_196.revapi.LY99_pad import microcrystal

  SS = spectra_simulation()
  C = microcrystal(Deff_A = 4000, length_um = 4., beam_diameter_um = 1.0) # assume smaller than 10 um crystals

  from LS49 import legacy_random_orientations
  random_orientations = legacy_random_orientations(N_total)
  transmitted_info = dict(spectra = SS,
                          crystal = C,
                          sfall_info = sfall_channels,
                          random_orientations = random_orientations)

  idx = 0
  tst_one(image=idx,spectra=transmitted_info["spectra"],
      crystal=transmitted_info["crystal"],
      random_orientation=transmitted_info["random_orientations"][idx],
      sfall_channels=transmitted_info["sfall_info"], params=params
  )


if __name__=="__main__":
  run_LY99_batch()
