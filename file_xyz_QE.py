# Import libraries
import os
import numpy as np
import matplotlib.pyplot as plt
# Import ASE library for read and write
import ase
from ase.io import read, write
from ase import Atoms
from ase.calculators.espresso import Espresso
# Import MDAnalysis for reading trajectory files
import MDAnalysis as mda

pseudopotentials = {'O': 'O.pbe-n-kjpaw_psl.0.1.UPF', 'H': 'H.pbe-rrkjus_psl.1.0.0.UPF', 'C': 'C.pbe-n-kjpaw_psl.1.0.0.UPF'}

# Create cell vectors from A, B, C
cell = [[40.0600000,         0.00000000,         0.0000000000],
       [0.000000000,         40.0600000,         0.0000000000],
       [0.000000000,         0.00000000,         40.060000000]]
#cell = [[40.0650, 0, 0], [0, 40.0650, 0], [0, 0, 40.0650]]


# Path to the XYZ trajectory file
trajectory_file = 'traj.xyz'

# Output directory for Quantum Espresso input files
output_dir = 'In_file'

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read the trajectory
universe = mda.Universe(trajectory_file)

# Iterate over each frame
for ts in universe.trajectory:
    print("Writing file for frame: ", ts.frame)
    # Convert MDAnalysis universe to ASE atoms
    atoms = Atoms(symbols=universe.atoms.names,
                  positions=universe.atoms.positions,
                  cell=cell,
                  pbc=True)
    outdir = os.path.join('scratch', str(ts.frame))
#    outdir = os.path.join(output_dir, str(ts.frame))
    pseudo_dir = '/path/to/pseudopotential/dir' # Change accordingly
    # Write Quantum Espresso input file for the current frame
    input_qe = {
        'calculation': 'scf',
        'outdir': outdir,
        'pseudo_dir': pseudo_dir,
        'tprnfor': True,
        'tstress': True,
        'disk_io': 'none',
        'system': {
            'ecutwfc': 30,
            'input_dft': 'PBE'
        },
        'electrons': {
            'mixing_beta': 0.5,
            'electron_maxstep': 1000
        }
    }

    write(os.path.join(output_dir, f"pw-wt-{ts.frame}.in"), atoms, format='espresso-in',
          input_data=input_qe, pseudopotentials=pseudopotentials)

