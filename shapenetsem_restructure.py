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
# # ShapeNetSem Restructure
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
#
# {input_shapenetsem_texture_dir}
# ├── 0004f1000ab18a48.jpg
# ├── 000b6c4b5b7a8dc3.jpg
# ├── 000c33be903cedc5.jpg
# ├── 000ec8dadff7bc1c.jpg
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
#
# ```
# Also, in addition to the .obj file, we also want to add in the .mtl file with the same name and the .jpg associated with the .mtl
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
# ## PIPELINE:
#
# 0. create new directory for restructured shapenetsem
# 1. for each acronym file, get the mesh filename (from acronym filename and from data within)
# 2. validate that the two mesh filenames match
# 3. copy mesh file from shapenetsem to new directory with correct directory name

# %%
import subprocess
import os
import h5py
from tqdm import tqdm

# %%
# INPUT PARAMS
input_acronym_dir = "/juno/u/tylerlum/github_repos/acronym/data/grasps/"
input_shapenetsem_dir = "/juno/u/tylerlum/github_repos/acronym/data/ShapeNetSem/models/"
input_shapenetsem_texture_dir = "/juno/u/tylerlum/github_repos/acronym/data/ShapeNetSem/textures/"
output_shapenetsem_dir = (
    "/juno/u/tylerlum/github_repos/acronym/data/ShapeNetSem_restructured/"
)

# %%
print("=" * 100)
print("PARAMS")
print("=" * 100)
print(f"input_acronym_dir: {input_acronym_dir}")
print(f"input_shapenetsem_dir: {input_shapenetsem_dir}")
print(f"input_shapenetsem_texture_dir: {input_shapenetsem_texture_dir}")
print(f"output_shapenetsem_dir: {output_shapenetsem_dir}")
print()

# %%
# Check inputs
if not os.path.exists(input_acronym_dir):
    print(f"input_acronym_dir: {input_acronym_dir} does not exist. Exiting.")
    exit()

if not os.path.exists(input_shapenetsem_dir):
    print(f"input_shapenetsem_dir: {input_shapenetsem_dir} does not exist. Exiting.")
    exit()

if not os.path.exists(input_shapenetsem_texture_dir):
    print(f"input_shapenetsem_texture_dir: {input_shapenetsem_texture_dir} does not exist. Exiting.")
    exit()

if os.path.exists(output_shapenetsem_dir):
    print(f"output_shapenetsem_dir: {output_shapenetsem_dir} already exists. Exiting.")
    exit()

# %%
print("=" * 100)
print("ACRONYM FILENAMES")
print("=" * 100)
acronym_filenames = os.listdir(input_acronym_dir)
print(f"Found {len(acronym_filenames)} files in {input_acronym_dir}")
print(f"First 10 acronym_filenames: {acronym_filenames[:10]}")
print()

# %%
# Get acronym obj filepaths from filename
print("=" * 100)
print("ACRONYM OBJ FILEPATHS FROM FILENAME")
print("=" * 100)
acronym_obj_filepaths = [
    os.path.join("meshes", filename.split("_")[0], filename.split("_")[1]) + ".obj"
    for filename in acronym_filenames
]
print(f"First 10 acronym_obj_filepaths: {acronym_obj_filepaths[:10]}")
print()

# %%
# Get acronym obj filepaths from within file
print("=" * 100)
print("ACRONYM OBJ FILEPATHS FROM WITHIN FILE")
print("=" * 100)
acronym_obj_filepaths_2 = []
for filename in tqdm(acronym_filenames):
    with h5py.File(os.path.join(input_acronym_dir, filename), "r") as f:
        obj_filepath = f["object/file"][()].decode("utf-8")
        acronym_obj_filepaths_2.append(obj_filepath)
print(f"First 10 acronym_obj_filepaths_2: {acronym_obj_filepaths_2[:10]}")

# %%
assert acronym_obj_filepaths == acronym_obj_filepaths_2
print("acronym_obj_filepaths == acronym_obj_filepaths_2")
print()

# %%
# Make output dir
print(f"Making output dir: {output_shapenetsem_dir}")
os.makedirs(output_shapenetsem_dir)
print(f"Done making output dir: {output_shapenetsem_dir}")

# %% jupyter={"outputs_hidden": true}
import re

def get_jpg_files_from_mtl(mtl_filepath):
    jpg_files = []
    with open(mtl_filepath, 'r') as f:
        mtl_data = f.read()
        matches = re.findall(r"map_K[ad]\s(.+\.jpg)", mtl_data)
        for match in matches:
            jpg_files.append(match)
    return jpg_files

# %%
num_failed = 0
for acronym_obj_filepath in (pbar := tqdm(acronym_obj_filepaths_2)):
    pbar.set_description(f"num_failed: {num_failed}")
    try:
        # Multiple acronym files for the same mesh, skip if already copied
        new_obj_filepath = os.path.join(output_shapenetsem_dir, acronym_obj_filepath)
        if os.path.exists(new_obj_filepath):
            print(
                f"Heads up: file {new_obj_filepath} already exists, but that is fine. Moving onto next file."
            )
            continue

        # Multiple meshes for the same category, continue
        new_dir = os.path.dirname(new_obj_filepath)
        if os.path.exists(new_dir):
            print(
                f"Heads up: dir {new_dir} already exists, but that is fine. Continuing."
            )
        os.makedirs(
            new_dir, exist_ok=True
        )  # can have more than one object in a category

        # Copy obj file
        cp_obj_command = " ".join(
            [
                "cp",
                os.path.join(input_shapenetsem_dir, os.path.basename(new_obj_filepath)),
                new_obj_filepath,
            ]
        )
        print(f"Running {cp_obj_command}")
        subprocess.run(cp_obj_command, check=True, shell=True)

        # Copy mtl file
        cp_mtl_command = cp_obj_command.replace('.obj', '.mtl')
        print(f"Running {cp_mtl_command}")
        subprocess.run(cp_mtl_command, check=True, shell=True)

        # Copy jpg file
        new_mtl_filepath = new_obj_filepath.replace('.obj', '.mtl')
        jpg_files = get_jpg_files_from_mtl(os.path.join(input_shapenetsem_dir, os.path.basename(new_mtl_filepath)))
        for jpg_file in jpg_files:
            cp_jpg_command = " ".join(
                    [
                        "cp",
                        os.path.join(input_shapenetsem_texture_dir, jpg_file),
                        os.path.join(os.path.dirname(new_obj_filepath), jpg_file),
                    ]
            )
            print(f"Running {cp_jpg_command}")
            subprocess.run(cp_jpg_command, check=True, shell=True)

    except subprocess.CalledProcessError as e:
        num_failed += 1
        print("=" * 100)
        print(f"Error: {e} when processing {acronym_obj_filepath}. Skipping it.")
        print("=" * 100)
        print()

# %%
