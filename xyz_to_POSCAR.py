#!/usr/bin/env python
import os
import argparse
from ase.io import write
from ase import Atoms
import MDAnalysis as mda

# Parse argument
# parser.add_argument("-b", "--box_size", type=float, default=12.0, help="Box size in Ang. (default: 12.0)")
parser = argparse.ArgumentParser(description="Write XYZ file with multiple frames to vasp POSCAR format")
parser.add_argument("-i", "--input", type=str, default="centered_structure.xyz", help="Input XYZ file containing multiple frames")
parser.add_argument("-b", "--box_size", type=float, nargs='+', default=[12.0], help="Box size in Ang. (defaulit Cubic : 12.0)")
args=parser.parse_args()

# Input file
trajectory_file = args.input     # default: centered_structure.xyz

# Periodic box
if len(args.box_size) == 1:
    # Cubic box
    box_a = box_b = box_c = args.box_size[0]
elif len(args.box_size) == 3:
    # Orthorombic box
    box_a, box_b, box_c = args.box_size
else:
    print('Error: parse 1 value for Cubic or 3 values for Orthorohmbic in box argument')
    exit(1)        

# check in Input file exist
if not os.path.isfile(trajectory_file):
    print(f'Error: Input file {trajectory_file} not found, exiting...')
    exit(1)
prefix_path = os.getcwd()
print("=============================================================")
print(f' Working directory : {prefix_path}')
print(f' Reading file : {trajectory_file}')
print(f' Box dimenstions : A = {box_a}, B = {box_b}, C = {box_c}')
print("=============================================================")

# Create cell vectors from A, B, C
cell = [[box_a, 0.0, 0.0],
        [0.0, box_b, 0.0],
        [0.0, 0.0, box_c]]

# Output directory for Quantum Espresso input files
output_dir = 'poscar_files'

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)

# Read the trajectory
universe = mda.Universe(trajectory_file)

# Iterate over each frame
for ts in universe.trajectory:
    # Convert MDAnalysis universe to ASE atoms
    print(f"# Converting xyz to POSCAR using MDAnalysis for structure {ts}")
    atoms = Atoms(symbols=universe.atoms.names,
                  positions=universe.atoms.positions,
                  cell=cell,
                  pbc=True)
#    print(ts.frame)
    outdir = os.path.join(output_dir, str(ts.frame))
    os.makedirs(outdir, exist_ok=True)
    write(os.path.join(outdir,f"POSCAR"), atoms, format='vasp')

print(f'POSCAR files written in directory, {output_dir}.')
