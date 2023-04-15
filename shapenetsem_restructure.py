# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import subprocess
import os
import h5py
from tqdm import tqdm

"""
INPUTS
---------------

{input_acronym_dir}
├── 1Shelves_12a64182bbaee7a12b2444829a3507de_0.00914554366969263.h5
├── 1Shelves_160684937ae737ec5057ad0f363d6ddd_0.009562610447288044.h5
├── 1Shelves_1e3df0ab57e8ca8587f357007f9e75d1_0.011099225885734912.h5
├── 1Shelves_2b9d60c74bc0d18ad8eae9bce48bbeed_0.00614208274225087.h5

{input_shapenetsem_dir}
├── 1004f30be305f33d28a1548e344f0e2e.mtl
├── 1004f30be305f33d28a1548e344f0e2e.obj
├── 100f39dce7690f59efb94709f30ce0d2.mtl
├── 100f39dce7690f59efb94709f30ce0d2.obj
"""

"""
OUTPUTS
---------------

{output_shapenetsem_dir}
└── meshes
    ├── Mug
    │   └── 10f6e09036350e92b3f21f1137c3c347.obj
    └── Table
        └── 99cf659ae2fe4b87b72437fd995483b.obj
"""

"""
NOTES:
---------------
* 24980 files in ShapeNetSem, half are mtl and half are obj, so total of 12490
* 8836 files in grasps from acronym
* each acronym file should have a corresponding shapenetsem file (8836 x 2 outputs for obj and mtl)
* each acronym file has a filename path to mesh file that looks like meshes/Mug/10f6e09036350e92b3f21f1137c3c347.obj
* the shapenetsem files have a name but they don't match exactly
"""

"""
PIPELINE:
---------------
0. create new directory for restructured shapenetsem
1. for each acronym file, get the mesh filename (from acronym filename and from data within)
2. validate that the two mesh filenames match
3. copy mesh file from shapenetsem to new directory with correct directory name
"""


# INPUT PARAMS
input_acronym_dir = "/juno/u/tylerlum/github_repos/acronym/data/grasps/"
input_shapenetsem_dir = "/juno/u/tylerlum/github_repos/acronym/data/ShapeNetSem/models/"
output_shapenetsem_dir = (
    "/juno/u/tylerlum/github_repos/acronym/data/ShapeNetSem_restructured/"
)

print("=" * 100)
print(f"PARAMS")
print("=" * 100)
print(f"input_acronym_dir: {input_acronym_dir}")
print(f"input_shapenetsem_dir: {input_shapenetsem_dir}")
print(f"output_shapenetsem_dir: {output_shapenetsem_dir}")
print()

# Check inputs
if not os.path.exists(input_acronym_dir):
    print(f"input_acronym_dir: {input_acronym_dir} does not exist. Exiting.")
    exit()

if not os.path.exists(input_shapenetsem_dir):
    print(f"input_shapenetsem_dir: {input_shapenetsem_dir} does not exist. Exiting.")
    exit()

if os.path.exists(output_shapenetsem_dir):
    print(f"output_shapenetsem_dir: {output_shapenetsem_dir} already exists. Exiting.")
    exit()

print("=" * 100)
print("ACRONYM FILENAMES")
print("=" * 100)
acronym_filenames = os.listdir(input_acronym_dir)
print(f"Found {len(acronym_filenames)} files in {input_acronym_dir}")
print(f"First 10 acronym_filenames: {acronym_filenames[:10]}")
print()

# Get acronym obj hashes from filename
print("=" * 100)
print("ACRONYM OBJ HASHES FROM FILENAME")
print("=" * 100)
acronym_obj_hashes = [
    os.path.join("meshes", filename.split("_")[0], filename.split("_")[1]) + ".obj"
    for filename in acronym_filenames
]
print(f"First 10 acronym_obj_hashes: {acronym_obj_hashes[:10]}")
print()

# Get acronym obj hashes from within file
print("=" * 100)
print("ACRONYM OBJ HASHES FROM FILENAME")
print("=" * 100)
acronym_obj_hashes_2 = []
for filename in tqdm(acronym_filenames):
    with h5py.File(os.path.join(input_acronym_dir, filename), "r") as f:
        obj_hash = f["object/file"][()].decode("utf-8")
        acronym_obj_hashes_2.append(obj_hash)
    if len(acronym_obj_hashes_2) == 10:
        break
print(f"First 10 acronym_obj_hashes_2: {acronym_obj_hashes_2[:10]}")

assert acronym_obj_hashes == acronym_obj_hashes_2
print("acronym_obj_hashes == acronym_obj_hashes_2")
print()

# Make output dir
print(f"Making output dir: {output_shapenetsem_dir}")
os.makedirs(output_shapenetsem_dir)
print(f"Done making output dir: {output_shapenetsem_dir}")

num_failed = 0
for acronym_obj_hash in (pbar := tqdm(acronym_obj_hashes_2)):
    pbar.set_description(f"num_failed: {num_failed}")
    try:
        os.makedirs(
            os.path.join(output_shapenetsem_dir, os.path.dirname(acronym_obj_hash))
        )
        cp_command = f"cp {os.path.join(input_shapenetsem_dir, os.path.basename(acronym_obj_hash))} {acronym_obj_hash}"
        print(f"Running {cp_command}")
        subprocess.run(cp_command, check=True, shell=True)

    except subprocess.CalledProcessError as e:
        num_failed += 1
        print("=" * 100)
        print(f"Error: {e} when processing {acronym_obj_hash}. Skipping it.")
        print("=" * 100)
        print()
