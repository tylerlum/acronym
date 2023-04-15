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
# # Meshes To URDFs
#
# ## INPUTS
#
# ```
# {input_shapenetsem_restructured_dir}
# └── meshes
#     ├── Mug
#     │   └── 10f6e09036350e92b3f21f1137c3c347.obj
#     │   └── 10f6e09036350e92b3f21f1137c3c347.mtl
#     └── Table
#         └── 99cf659ae2fe4b87b72437fd995483b.obj
#         └── 99cf659ae2fe4b87b72437fd995483b.mtl
# ```
#
# Also, may have .jpg files associated with the .mtl files
#
# Another input is object_scaling (these objects are quite huge by default in isaac gym)
#
# ## OUTPUTS
#
# {output_urdf_dir}
# ```
# {input_shapenetsem_restructured_dir}
# └── urdf
#     ├── Mug.urdf
#     └── Table.urdf
# ```
#
# ## NOTES
#
# * Each folder within `meshes` (eg. `meshes/Mug`) may have multiple .obj files (and other files)
#
# Example:
#
# ```
# ls meshes/Mug | grep obj
# 10f6e09036350e92b3f21f1137c3c347.obj
# 128ecbc10df5b05d96eaf1340564a4de.obj
# 159e56c18906830278d8f8c02c47cde0.obj
# 187859d3c3a2fd23f54e1b6f41fdd78a.obj
# 1ea9ea99ac8ed233bf355ac8109b9988.obj
# 2073dd06f62b46d43c8079bde16af00d.obj
# 23fb2a2231263e261a9ac99425d3b306.obj
# ...
# ```
#
# * urdf files should looks like:
#
# ```
# <?xml version="1.0"?>
# <robot name="banana">
#   <link name="base">
#     <visual>
#       <origin xyz="0 0 0"/>
#       <geometry>
#         <mesh filename="meshes/banana/textured.obj"/>
#       </geometry>
#     </visual>
#     <collision>
#       <origin xyz="0 0 0"/>
#       <geometry>
#         <mesh filename="meshes/banana/textured.obj"/>
#       </geometry>
#     </collision>
#     <inertial>
#         <density value="600.0"/>
#     </inertial>
#   </link>
# </robot>
# ```
#
# ## PIPELINE
#
# 0. create new directory for `urdf`
#
# 1. for each .obj file, create a .urdf file that points to it. TODO: figure out how to handle multiple obj files. Could just use 1 or make many urdfs (eg. urdf/Mug_10f6e09036350e92b3f21f1137c3c347.urdf, urdf/Mug_128ecbc10df5b05d96eaf1340564a4de.urdf)
#

# %%
import os
from tqdm import tqdm

# %%
# INPUT PARAMS
input_shapenetsem_restructured_dir = (
    "/juno/u/tylerlum/github_repos/acronym/data/ShapeNetSem_restructured"
)
object_scaling = 0.01

# %%
print("=" * 100)
print("PARAMS")
print("=" * 100)
print(f"input_shapenetsem_restructured_dir: {input_shapenetsem_restructured_dir}")
print()

# %%
# Check inputs
if not os.path.exists(input_shapenetsem_restructured_dir):
    print(
        f"input_shapenetsem_restructured_dir: {input_shapenetsem_restructured_dir} does not exist. Exiting."
    )
    exit()

input_meshes_dir = os.path.join(input_shapenetsem_restructured_dir, "meshes")
if not os.path.exists(input_meshes_dir):
    print(f"input_meshes_dir: {input_meshes_dir} does not exist. Exiting.")
    exit()

print("=" * 100)
print("OBJECT CATEGORY FOLDERS")
print("=" * 100)
object_categories = os.listdir(input_meshes_dir)
print(f"Found {len(object_categories)} files in {input_meshes_dir}")
print(f"First 10 object_categories: {object_categories[:10]}")
print()

# %%
# Make output dir
output_urdf_dir = os.path.join(input_shapenetsem_restructured_dir, "urdf")
if os.path.exists(output_urdf_dir):
    print(f"output_urdf_dir: {output_urdf_dir} already exists. Exiting.")
    exit()

print(f"Making output dir: {output_urdf_dir}")
os.makedirs(output_urdf_dir)
print(f"Done making output dir: {output_urdf_dir}")

# %%
num_failed = 0
for object_category in tqdm(object_categories):
    object_category_dir = os.path.join(input_meshes_dir, object_category)

    for object_file in os.listdir(object_category_dir):
        object_category_file_without_ext, ext = os.path.splitext(object_file)
        if ext != ".obj":
            continue

        object_name = f"{object_category}_{object_category_file_without_ext}"
        print(f"Processing object_name: {object_name}")

        mesh_filepath = os.path.join(object_category_dir, object_file).split("/")
        meshes_idx = mesh_filepath.index("meshes")
        mesh_filepath = os.path.join(*mesh_filepath[meshes_idx:])
        object_urdf_filepath = os.path.join(output_urdf_dir, f"{object_name}.urdf")
        print(f"Creating urdf file: {object_urdf_filepath}")
        print(f"Setting mesh_filepath to: {mesh_filepath}")

        with open(object_urdf_filepath, "w") as f:
            urdf_text = "\n".join(
                [
                    '<?xml version="1.0"?>',
                    f'<robot name="{object_name}">',
                    '  <link name="base">',
                    "    <visual>",
                    '      <origin xyz="0 0 0"/>',
                    "      <geometry>",
                    f'        <mesh filename="{mesh_filepath}" scale="{object_scaling} {object_scaling} {object_scaling}" />',
                    "      </geometry>",
                    "    </visual>",
                    "    <collision>",
                    '      <origin xyz="0 0 0"/>',
                    "      <geometry>",
                    f'        <mesh filename="{mesh_filepath}" scale="{object_scaling} {object_scaling} {object_scaling}" />',
                    "      </geometry>",
                    "    </collision>",
                    "    <inertial>",
                    '        <density value="600.0"/>',
                    "    </inertial>",
                    "  </link>",
                    "</robot>",
                ]
            )

            f.write(urdf_text)
