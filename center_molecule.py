import numpy as np
import os
import argparse

# ParseArgument 
#parser.add_argument("-i", "--input", type=str, required=True, help="Input XYZ trajectory file")
parser = argparse.ArgumentParser(description="Center molecular structure within PBC")
parser.add_argument("-i", "--input", type=str, default="trajec.xyz", help="Input XYZ trajectory file")
parser.add_argument("-o", "--output", type=str, default='centered_structure.xyz', help="Output XYZ trajectory file")
parser.add_argument("-b", "--box_size", type=float, default=12.0, help="Box size in Ang. (default: 15.0)")
args = parser.parse_args()


# Define the input and output file names and box size
input_file = args.input    # trajec.xyz
output_file = args.output # centered_structure.xyz
box_size = args.box_size   # 15.0  # Box size in Å

# check if input file exist
if not os.path.isfile(input_file):
    print(f'Error: Input file {input_file} not found')
    exit(1)
# Load your structure file (assuming it's in XYZ format)
with open(input_file, "r") as file:
    lines = file.readlines()

print('==============================')
print(f'Reading... {input_file}')
print('==============================')
# Initialize variables
frames = []
i = 0

# Read through lines to extract frames
while i < len(lines):
    if lines[i].strip().isdigit():  # Number of atoms line
        num_atoms = int(lines[i].strip())
        title = lines[i + 1].strip()
        atom_types = []
        coordinates = []

        for j in range(num_atoms):
            parts = lines[i + 2 + j].split()
            if len(parts) == 4:
                atom_types.append(parts[0])
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                coordinates.append([x, y, z])
            else:
                print(f"Warning: Skipping line due to incorrect format: {lines[i + 2 + j].strip()}")

        # Convert coordinates to NumPy array for easier manipulation
        coordinates = np.array(coordinates)

        # Calculate the center of mass of the molecule
        center_of_mass = np.mean(coordinates, axis=0)

        # Calculate the shift needed to center the molecule within the periodic boundary conditions
        shift = np.array([box_size / 2, box_size / 2, box_size / 2]) - center_of_mass

        # Shift coordinates to center the molecule within the periodic boundary conditions
        coordinates_shifted = coordinates + shift

        # Store the frame data
        frames.append((num_atoms, title, atom_types, coordinates_shifted))

        # Move to the next frame
        i += 2 + num_atoms
    else:
        print(f"Warning: Skipping unexpected line: {lines[i].strip()}")
        i += 1

# Save the modified trajectory in XYZ format
with open(output_file, "w") as file:
    for num_atoms, title, atom_types, coordinates_shifted in frames:
        file.write(f"{num_atoms}\n")
        file.write(f"{title}\n")
        for k in range(num_atoms):
            atom_line = f"{atom_types[k]} {coordinates_shifted[k][0]:.3f} {coordinates_shifted[k][1]:.3f} {coordinates_shifted[k][2]:.3f}\n"
            file.write(atom_line)

print(f'Centered structure saved in {output_file} wihtin periodic box {box_size}')
