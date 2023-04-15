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

# %% [markdown]
# # Watertight ShapeNetSem
#
# ## INPUTS
#
# ```
# {input_acronym_dir}
# ├── 1Shelves_12a64182bbaee7a12b2444829a3507de_0.00914554366969263.h5
# ├── 1Shelves_160684937ae737ec5057ad0f363d6ddd_0.009562610447288044.h5
# ├── 1Shelves_1e3df0ab57e8ca8587f357007f9e75d1_0.011099225885734912.h5
# ├── 1Shelves_2b9d60c74bc0d18ad8eae9bce48bbeed_0.00614208274225087.h5
#
# {input_shapenetsem_dir}
# ├── 1004f30be305f33d28a1548e344f0e2e.mtl
# ├── 1004f30be305f33d28a1548e344f0e2e.obj
# ├── 100f39dce7690f59efb94709f30ce0d2.mtl
# ├── 100f39dce7690f59efb94709f30ce0d2.obj
# ```
#
# ## OUTPUTS
#
# ```
# {output_shapenetsem_dir}
# └── meshes
#     ├── Mug
#     │   └── 10f6e09036350e92b3f21f1137c3c347.obj
#     └── Table
#         └── 99cf659ae2fe4b87b72437fd995483b.obj
# ```
#
# ## NOTES
#
# * 24980 files in ShapeNetSem, half are mtl and half are obj, so total of 12490
# * 8836 files in grasps from acronym
# * each acronym file should have a corresponding shapenetsem file (8836 x 2 outputs for obj and mtl)
# * each acronym file has a filename path to mesh file that looks like meshes/Mug/10f6e09036350e92b3f21f1137c3c347.obj
# * the shapenetsem files have a name but they don't match exactly
# * there can be more than one mesh per category (eg. multiple under the TV directory)
# * there can also be more than one acronym file per mesh (eg. multiple grasps for the same mesh )
#   eg. "data/grasps/TV_dfbce5e6cca00c1448627a76b6268107_0.0038627305095302734.h5"
#       "data/grasps/TV_dfbce5e6cca00c1448627a76b6268107_0.003957748840105706.h5"
#
# SHOULD USE MANIFOLD (https://github.com/hjwdzh/Manifold), BUILD, AND COPY THIS SCRIPT TO THE MANIFOLD ROOT DIRECTORY


# %%
import subprocess
import os
from tqdm import tqdm
from typing import DefaultDict


# %%
# INPUT PARAMS
input_acronym_dir = "/juno/u/tylerlum/github_repos/acronym/data/grasps/"
input_shapenetsem_dir = "/juno/u/tylerlum/github_repos/acronym/data/ShapeNetSem/models/"
temp_watertight_obj_filename = "temp.watertight.obj"
output_watertight_shapenetsem_dir = "WatertightShapeNetSem/models"

# %%
print("=" * 100)
print(f"PARAMS")
print("=" * 100)
print(f"input_acronym_dir: {input_acronym_dir}")
print(f"input_shapenetsem_dir: {input_shapenetsem_dir}")
print(f"temp_watertight_obj_filename: {temp_watertight_obj_filename}")
print(f"output_watertight_shapenetsem_dir: {output_watertight_shapenetsem_dir}")
print()

# %%
# Check inputs
if not os.path.exists(input_acronym_dir):
    print(f"input_acronym_dir: {input_acronym_dir} does not exist. Exiting.")
    exit()

if not os.path.exists(input_shapenetsem_dir):
    print(f"input_shapenetsem_dir: {input_shapenetsem_dir} does not exist. Exiting.")
    exit()

if os.path.exists(temp_watertight_obj_filename):
    print(
        f"temp_watertight_obj_filename: {temp_watertight_obj_filename} already exists. Removing it and continuing."
    )
    subprocess.run(f"rm {temp_watertight_obj_filename}", shell=True, check=True)

if os.path.exists(output_watertight_shapenetsem_dir):
    print(
        f"output_watertight_shapenetsem_dir: {output_watertight_shapenetsem_dir} already exists. Exiting."
    )
    exit()

# %%
# Get acronym obj hashes
print("=" * 100)
print(f"ACRONYM OBJ HASHES")
print("=" * 100)
acronym_filenames = os.listdir(input_acronym_dir)
print(f"Found {len(acronym_filenames)} files in {input_acronym_dir}")
print(f"First 10 acronym_filenames: {acronym_filenames[:10]}")
acronym_obj_hashes = [filename.split("_")[1] for filename in acronym_filenames]
print(f"First 10 acronym_obj_hashes: {acronym_obj_hashes[:10]}")

# %%
# Print information about acronym obj hashes (some may be off)
len_to_hashes = DefaultDict(list)
for obj_hash in acronym_obj_hashes:
    len_to_hashes[len(obj_hash)].append(obj_hash)
len_to_freq = {length: len(hashes) for length, hashes in len_to_hashes.items()}
print(f"len_to_freq: {len_to_freq}")
print("Example of each:")
for length, hashes in len_to_hashes.items():
    print(f"length: {length}, hash: {hashes[0]}")
acronym_obj_hashes = set(acronym_obj_hashes)
print()

# %%
# Get all filenames
print("=" * 100)
print(f"SHAPENET FILENAMES")
print("=" * 100)
shapenet_filenames = os.listdir(input_shapenetsem_dir)
print(f"Found {len(shapenet_filenames)} files in {input_shapenetsem_dir}")
print(f"First 10 shapenet_filenames: {shapenet_filenames[:10]}")
shapenet_filenames.sort()

# %%
obj_filenames = [
    filename for filename in shapenet_filenames if filename.endswith(".obj")
]
mtl_filenames = [
    filename for filename in shapenet_filenames if filename.endswith(".mtl")
]
assert len(obj_filenames) == len(mtl_filenames)

# %%
# Sanity check
for obj_filename, mtl_filename in zip(obj_filenames, mtl_filenames):
    obj_filename_without_ext, obj_ext = os.path.splitext(obj_filename)
    mtl_filename_without_ext, mtl_ext = os.path.splitext(mtl_filename)
    assert obj_filename_without_ext == mtl_filename_without_ext
    assert obj_ext == ".obj"
    assert mtl_ext == ".mtl"

# %%
# Filter out non-acronym obj hashes
obj_filenames = [
    obj_filename
    for obj_filename in obj_filenames
    if os.path.splitext(obj_filename)[0] in acronym_obj_hashes
]
mtl_filenames = [
    mtl_filename
    for mtl_filename in mtl_filenames
    if os.path.splitext(mtl_filename)[0] in acronym_obj_hashes
]
print(
    f"Filtered down to {len(obj_filenames)} obj_filenames and {len(mtl_filenames)} mtl_filenames"
)
print()

# %%
# Make output dir
print(f"Making output dir: {output_watertight_shapenetsem_dir}")
os.makedirs(output_watertight_shapenetsem_dir)
print(f"Done making output dir: {output_watertight_shapenetsem_dir}")

# %%
num_failed = 0
for obj_filename, mtl_filename in (
    pbar := tqdm(zip(obj_filenames, mtl_filenames), total=len(obj_filenames))
):
    pbar.set_description(f"num_failed: {num_failed}")
    try:
        obj_filename_without_ext, obj_ext = os.path.splitext(obj_filename)
        mtl_filename_without_ext, mtl_ext = os.path.splitext(mtl_filename)
        assert obj_filename_without_ext == mtl_filename_without_ext
        assert obj_ext == ".obj"
        assert mtl_ext == ".mtl"

        input_obj_filepath = os.path.join(input_shapenetsem_dir, obj_filename)
        watertight_mesh_command = (
            f"./build/manifold {input_obj_filepath} {temp_watertight_obj_filename} -s"
        )
        print(f"watertight_mesh_command: {watertight_mesh_command}")
        subprocess.run(watertight_mesh_command, shell=True, check=True)

        output_obj_filepath = os.path.join(
            output_watertight_shapenetsem_dir, obj_filename
        )
        simplify_command = f"./build/simplify -i {temp_watertight_obj_filename} -o {output_obj_filepath} -m -r 0.02"
        print(f"simplify_command: {simplify_command}")
        subprocess.run(simplify_command, shell=True, check=True)

        rm_command = f"rm {temp_watertight_obj_filename}"
        subprocess.run(rm_command, shell=True, check=True)

        print()
    except subprocess.CalledProcessError as e:
        num_failed += 1
        print("=" * 100)
        print(
            f"Error: {e} when processing {obj_filename} and {mtl_filename}. Skipping it."
        )
        print("=" * 100)
        print()
