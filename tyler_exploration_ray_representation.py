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
# # ACRONYM Dataset Exploration Ray Representation

# %% [markdown]
# ## Input Params

# %%
mesh_root = "data/ShapeNetSem_restructured/"
filepath = "data/grasps/AAABattery_a924eb3037129eaff8095890d92b7d6c_0.09387254242350625.h5"
num_grasps = 20

# %%
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
MAGENTA = [255, 0, 255]

# %% [markdown]
# ## Read Mesh

# %%
import h5py
import trimesh
import os

# Read in mesh
scale = None
data = h5py.File(filepath, "r")
mesh_fname = data["object/file"][()].decode('utf-8')
mesh_scale = data["object/scale"][()] if scale is None else scale
obj_mesh = trimesh.load(os.path.join(mesh_root, mesh_fname))
obj_mesh = obj_mesh.apply_scale(mesh_scale)

# %%
obj_mesh

# %% [markdown]
# ## Read Grasps

# %%
# Get grasps
import numpy as np
transforms = np.array(data["grasps/transforms"])
success = np.array(data["grasps/qualities/flex/object_in_gripper"])

# %%
transforms.shape

# %%
success.shape

# %% [markdown]
# ## Visualize Grasps

# %%
# Visualize grasps
from acronym_tools import create_gripper_marker, create_gripper_tips_marker
successful_grasps = [
    create_gripper_marker(color=GREEN).apply_transform(t)
    for t in transforms[np.random.choice(np.where(success == 1)[0], num_grasps)]
]
failed_grasps = [
    create_gripper_marker(color=RED).apply_transform(t)
    for t in transforms[np.random.choice(np.where(success == 0)[0], num_grasps)]
]

trimesh.Scene([obj_mesh] + successful_grasps + failed_grasps).show()

# %% [markdown]
# # Visualize Grasps w/ Rays

# %%
# Visualize identity transform grasp, identity + z translation, identity + z + x translation
identity = np.eye(4)

identity_plus_z = np.eye(4)
identity_plus_z[:3, 3] = [0.0, 0.0, 0.1]

identity_plus_xz = np.eye(4)
identity_plus_xz[:3, 3] = [0.1, 0.0, 0.1]

transform_color_pairs = [
    (identity, RED),
    (identity_plus_z, GREEN),
    (identity_plus_xz, BLUE),
]

grasps = [
    create_gripper_marker(color=color).apply_transform(transform)
    for transform, color in transform_color_pairs
]

# Visualize grasp tips and inward directions
tips = [
    create_gripper_tips_marker(color=BLUE).apply_transform(transform)
    for transform, _ in transform_color_pairs
]

trimesh.Scene([obj_mesh] + grasps + tips).show()



# %%
import trimesh
# Visualize identity transform grasp, identity + z translation, identity + z + x translation
identity = np.eye(4)

identity_plus_z = np.eye(4)
identity_plus_z[:3, 3] = [0.0, 0.0, 0.1]

identity_plus_xz = np.eye(4)
identity_plus_xz[:3, 3] = [0.1, 0.0, 0.1]

transform_color_pairs = [
    (identity, RED),
    (identity_plus_z, GREEN),
    (identity_plus_xz, BLUE),
]

grasps = [
    create_gripper_marker(color=color).apply_transform(transform)
    for transform, color in transform_color_pairs
]

# Visualize grasp tips and inward directions using math
left_tip_pos = [4.10000000e-02, -7.27595772e-12, 1.12169998e-01]
right_tip_pos = [-4.10000000e-02, -7.27595772e-12, 1.12169998e-01]
left_tip_dir_end = [4.10000000e-02 * 0.7, -7.27595772e-12, 1.12169998e-01]
right_tip_dir_end = [-4.10000000e-02 * 0.7, -7.27595772e-12, 1.12169998e-01]

tips = []
for transform, _ in transform_color_pairs:
    # Transform
    left_tip_pos_transformed = (transform @ np.array([*left_tip_pos, 1.0]))[:3]
    right_tip_pos_transformed = (transform @ np.array([*right_tip_pos, 1.0]))[:3]
    left_tip_dir_end_transformed = (transform @ np.array([*left_tip_dir_end, 1.0]))[:3]
    right_tip_dir_end_transformed = (transform @ np.array([*right_tip_dir_end, 1.0]))[:3]

    # Create cylinders
    left_ray = trimesh.creation.cylinder(
        radius=0.002,
        sections=6,
        segment=[
            left_tip_pos_transformed,
            left_tip_dir_end_transformed,
        ],
    )
    right_ray = trimesh.creation.cylinder(
        radius=0.002,
        sections=6,
        segment=[
            right_tip_pos_transformed,
            right_tip_dir_end_transformed,
        ],
    )
    tmp = trimesh.util.concatenate([left_ray, right_ray])
    tmp.visual.face_colors = MAGENTA
    tips.append(tmp)

trimesh.Scene([obj_mesh] + grasps + tips).show()


# %%
# Visualize grasps w/ rays

successful_transforms = transforms[np.random.choice(np.where(success == 1)[0], num_grasps)]
failed_transforms = transforms[np.random.choice(np.where(success == 0)[0], num_grasps)]

successful_grasps = [
    create_gripper_marker(color=GREEN).apply_transform(t)
    for t in successful_transforms
]
failed_grasps = [
    create_gripper_marker(color=RED).apply_transform(t)
    for t in failed_transforms
]

# Visualize grasp tips and inward directions using math
left_tip_pos = [4.10000000e-02, -7.27595772e-12, 1.12169998e-01]
right_tip_pos = [-4.10000000e-02, -7.27595772e-12, 1.12169998e-01]
left_tip_dir_end = [4.10000000e-02 * 0.7, -7.27595772e-12, 1.12169998e-01]
right_tip_dir_end = [-4.10000000e-02 * 0.7, -7.27595772e-12, 1.12169998e-01]

tips = []
for transform in list(successful_transforms) + list(failed_transforms):
    # Transform
    left_tip_pos_transformed = (transform @ np.array([*left_tip_pos, 1.0]))[:3]
    right_tip_pos_transformed = (transform @ np.array([*right_tip_pos, 1.0]))[:3]
    left_tip_dir_end_transformed = (transform @ np.array([*left_tip_dir_end, 1.0]))[:3]
    right_tip_dir_end_transformed = (transform @ np.array([*right_tip_dir_end, 1.0]))[:3]

    # Create cylinders
    left_ray = trimesh.creation.cylinder(
        radius=0.002,
        sections=6,
        segment=[
            left_tip_pos_transformed,
            left_tip_dir_end_transformed,
        ],
    )
    right_ray = trimesh.creation.cylinder(
        radius=0.002,
        sections=6,
        segment=[
            right_tip_pos_transformed,
            right_tip_dir_end_transformed,
        ],
    )
    tmp = trimesh.util.concatenate([left_ray, right_ray])
    tmp.visual.face_colors = MAGENTA
    tips.append(tmp)

trimesh.Scene([obj_mesh] + successful_grasps + failed_grasps + tips).show()

# %% [markdown]
# ## Look Into HDF5 File

# %%
data.keys()


# %%
def print_attrs(name, obj):
    if isinstance(obj, h5py.Group):
        print(name)
    else:
        print(f"{name}: {obj.shape}")

data.visititems(print_attrs)

# %%
root_keys = []
def store_root_keys(name, obj):
    if not isinstance(obj, h5py.Group):
        root_keys.append(name)

data.visititems(store_root_keys)
root_keys

# %%
root_keys_with_multiple_values = [key for key in root_keys if len(data[key].shape) > 0]
root_keys_with_multiple_values

# %%
root_keys_with_single_value = [key for key in root_keys if key not in root_keys_with_multiple_values]
root_keys_with_single_value

# %%
import matplotlib.pyplot as plt
import math
import numpy as np
num_plots = len(root_keys_with_multiple_values)
num_rows = int(math.sqrt(num_plots))
num_cols = int(math.ceil(num_plots / num_rows))

fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(20, 20))
axes = axes.flatten()
for i, root_key_with_multiple_values in enumerate(root_keys_with_multiple_values):
    ax = axes[i]
    ax.hist(np.array(data[root_key_with_multiple_values]).flatten())
    ax.set_title(root_key_with_multiple_values)

fig.tight_layout()

# %%
for root_key_with_single_value in root_keys_with_single_value:
    print(f"{root_key_with_single_value}: {data[root_key_with_single_value][()]}")

# %%

# %%

# %%
