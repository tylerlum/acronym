[ACRONYM](https://sites.google.com/nvidia.com/graspdataset) is a dataset of 17.7M simulated parallel-jaw grasps of 8872 objects. It was generated using [NVIDIA FleX](https://developer.nvidia.com/flex).

This repository contains a sample of the grasping dataset and tools to visualize grasps, generate random scenes, and render observations.

For using the full ACRONYM dataset, see instructions [below](#using-the-full-acronym-dataset).

# Tyler Updates (2023-06-13)

Follow the original README as usual. There are a few key useful things added. Note that these can be run as python scripts or as jupyter notebooks (should be run from `tyler_useful_scripts`):

## 0. Get ACRONYM Dataset

Follow instructions [here](https://sites.google.com/nvidia.com/graspdataset) to get the ACRONYM dataset and ShapeNetSem meshes.

Should have the following directory structure:

```
acronym/data/grasps
├── 1Shelves_12a64182bbaee7a12b2444829a3507de_0.00914554366969263.h5
├── 1Shelves_160684937ae737ec5057ad0f363d6ddd_0.009562610447288044.h5
├── 1Shelves_1e3df0ab57e8ca8587f357007f9e75d1_0.011099225885734912.h5
├── 1Shelves_2b9d60c74bc0d18ad8eae9bce48bbeed_0.00614208274225087.h5
├── 1Shelves_4075b78276e39db2f59ac8a5783023e7_0.003873753800979896.h5
├── 1Shelves_842be31d76d29df0a00888d2bacdd893_0.002664003835872925.h5
├── 1Shelves_a9c2bcc286b68ee217a3b9ca1765e2a4_0.004318170833733851.h5
├── 1Shelves_a9c2bcc286b68ee217a3b9ca1765e2a4_0.007691275299398608.h5
├── 1Shelves_ba5bf7a8a14c27086f9e9f74beb7c348_0.006726669391824365.h5
```

```
acronym/data/ShapeNetSem
├── categories.synset.csv
├── COLLADA
├── models
│   ├── 1004f30be305f33d28a1548e344f0e2e.mtl
│   ├── 1004f30be305f33d28a1548e344f0e2e.obj
│   ├── 100f39dce7690f59efb94709f30ce0d2.mtl
│   ├── 100f39dce7690f59efb94709f30ce0d2.obj
│   ├── 101354f9d8dede686f7b08d9de913afe.mtl
│   ├── 101354f9d8dede686f7b08d9de913afe.obj
│   ├── 1018f01d42ae7fad52249d8432f6087e.mtl
│   ├── 1018f01d42ae7fad52249d8432f6087e.obj
│   ├── 102273fdf8d1b90041fbc1e2da054acb.mtl
├── textures
│   ├── 0004f1000ab18a48.jpg
│   ├── 000b6c4b5b7a8dc3.jpg
│   ├── 000c33be903cedc5.jpg
│   ├── 000ec8dadff7bc1c.jpg
│   ├── 000f125dd68e7f10.jpg
│   ├── 00112bf8e3be136d.jpg
│   ├── 0011e285da6ba6d9.jpg
│   ├── 001421a14600e6e4.jpg
│   ├── 00181a83c3090fda.jpg
```

## 1. Watertight Meshes (Optional: Didn't work for me)

Run
```
python watertight_shapenetsem.py
```

This creates watertight meshes as per ACRONYM instructions (need to set up manifold). About half of them failed for me for some reason, so I skipped this step.

## 2. Restructure ShapeNetSem

Run
```
python shapenetsem_restructure.py
```

This changes the directory structure to be useful for future steps (more detail in script).

## 3. Create URDFs

Run
```
python meshes_to_urdfs.py
```

This creates a urdf for each of the meshes in a nice structure ready for use in simulators.

Lastly, you can move this `../data/ShapeNetSem_restructured` (this is default) directory into the `nerf_grasping/assets/objects` directory (other project), so you will have `nerf_grasping/assets/objects/meshes` and `nerf_grasping/assets/objects/urdf`.

All set for use in nerf_grasping.

## Exploration

Also, there are some scripts in `tyler_exploration_scripts` that may be useful for debugging and understanding the ACRONYM dataset.

# BELOW: Original README

# License
The source code is released under [MIT License](LICENSE). The dataset is released under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/legalcode).

# Requirements
* Python3
* `python -m pip install -r requirements.txt`

# Installation
* `python -m pip install -e .`

# Use Cases

### Visualize Grasps
```
usage: acronym_visualize_grasps.py [-h] [--num_grasps NUM_GRASPS] input [input ...]

Visualize grasps from the dataset.

positional arguments:
  input                 HDF5 or JSON Grasp file(s).

optional arguments:
  -h, --help            show this help message and exit
  --num_grasps NUM_GRASPS
                        Number of grasps to show. (default: 20)
  --mesh_root MESH_ROOT
                        Directory used for loading meshes. (default: .)
```

#### Examples
The following command shows 40 grasps for a mug from the dataset. Grasp markers are colored green/red based on whether the simulation result was a success/failure:

`acronym_visualize_grasps.py --mesh_root data/examples/ data/examples/grasps/Mug_10f6e09036350e92b3f21f1137c3c347_0.0002682457830986903.h5`

### Generate Random Scenes and Visualize Grasps
```
usage: generate_scene.py [-h] [--objects OBJECTS [OBJECTS ...]] --support
                         SUPPORT [--support_scale SUPPORT_SCALE]
                         [--show_grasps]
                         [--num_grasps_per_object NUM_GRASPS_PER_OBJECT]

Generate a random scene arrangement and filtering grasps that are in
collision.

optional arguments:
  -h, --help            show this help message and exit
  --objects OBJECTS [OBJECTS ...]
                        HDF5 or JSON Object file(s). (default: None)
  --support SUPPORT     HDF5 or JSON File for support object. (default: None)
  --support_scale SUPPORT_SCALE
                        Scale factor of support mesh. (default: 0.025)
  --mesh_root MESH_ROOT
                        Directory used for loading meshes. (default: .)
  --show_grasps         Show all grasps that are not in collision. (default:
                        False)
  --num_grasps_per_object NUM_GRASPS_PER_OBJECT
                        Maximum number of grasps to show per object. (default:
                        20)
```

#### Examples
This will show a randomly generated scene with a table as a support mesh and four mugs placed on top of it:

`acronym_generate_scene.py --mesh_root data/examples/ --objects data/examples/grasps/Mug_10f6e09036350e92b3f21f1137c3c347_0.0002682457830986903.h5 data/examples/grasps/Mug_10f6e09036350e92b3f21f1137c3c347_0.0002682457830986903.h5 data/examples/grasps/Mug_10f6e09036350e92b3f21f1137c3c347_0.0002682457830986903.h5 data/examples/grasps/Mug_10f6e09036350e92b3f21f1137c3c347_0.0002682457830986903.h5 --support data/examples/grasps/Table_99cf659ae2fe4b87b72437fd995483b_0.009700376721042367.h5`

Same as above but also showing green grasp markers (maximum: 20 per object) for successful grasps (filtering those that are in collision):

`acronym_generate_scene.py --mesh_root data/examples/ --objects data/examples/grasps/Mug_10f6e09036350e92b3f21f1137c3c347_0.0002682457830986903.h5 data/examples/grasps/Mug_10f6e09036350e92b3f21f1137c3c347_0.0002682457830986903.h5 data/examples/grasps/Mug_10f6e09036350e92b3f21f1137c3c347_0.0002682457830986903.h5 data/examples/grasps/Mug_10f6e09036350e92b3f21f1137c3c347_0.0002682457830986903.h5 --support data/examples/grasps/Table_99cf659ae2fe4b87b72437fd995483b_0.009700376721042367.h5 --show_grasps`

### Render and Visualize Observations
```
usage: render_observations.py [-h] [--objects OBJECTS [OBJECTS ...]] --support
                              SUPPORT [--support_scale SUPPORT_SCALE]
                              [--show_scene]

Render observations of a randomly generated scene.

optional arguments:
  -h, --help            show this help message and exit
  --objects OBJECTS [OBJECTS ...]
                        HDF5 or JSON Object file(s). (default: None)
  --support SUPPORT     HDF5 or JSON File for support object. (default: None)
  --support_scale SUPPORT_SCALE
                        Scale factor of support mesh. (default: 0.025)
  --mesh_root MESH_ROOT
                        Directory used for loading meshes. (default: .)
  --show_scene          Show the scene and camera pose from which observations
                        are rendered. (default: False)
```

#### Examples
This will show RGB image, depth, image and segmentation mask rendered from a random viewpoint):

`acronym_render_observations.py --mesh_root data/examples/ --objects data/examples/grasps/Mug_10f6e09036350e92b3f21f1137c3c347_0.0002682457830986903.h5 data/examples/grasps/Mug_10f6e09036350e92b3f21f1137c3c347_0.0002682457830986903.h5 data/examples/grasps/Mug_10f6e09036350e92b3f21f1137c3c347_0.0002682457830986903.h5 --support data/examples/grasps/Table_99cf659ae2fe4b87b72437fd995483b_0.009700376721042367.h5`

Same as above but also visualizes the scene and camera position in 3D:

`acronym_render_observations.py --mesh_root data/examples/ --objects data/examples/grasps/Mug_10f6e09036350e92b3f21f1137c3c347_0.0002682457830986903.h5 data/examples/grasps/Mug_10f6e09036350e92b3f21f1137c3c347_0.0002682457830986903.h5 data/examples/grasps/Mug_10f6e09036350e92b3f21f1137c3c347_0.0002682457830986903.h5 --support data/examples/grasps/Table_99cf659ae2fe4b87b72437fd995483b_0.009700376721042367.h5 --show_scene`


# Using the full ACRONYM dataset

1. Download the full dataset (1.6GB): [acronym.tar.gz](https://drive.google.com/file/d/1zcPARTCQx2oeiKk7a-wdN_CN-RUVX56c/view?usp=sharing)
2. Download the ShapeNetSem meshes from https://www.shapenet.org/
3. Create watertight versions of the downloaded meshes:
   1. Clone and build: https://github.com/hjwdzh/Manifold
   2. Create a watertight mesh version assuming the object path is model.obj: `manifold model.obj temp.watertight.obj -s`
   3. Simplify it: `simplify -i temp.watertight.obj -o model.obj -m -r 0.02`

For more details about the structure of the ACRONYM dataset see: https://sites.google.com/nvidia.com/graspdataset


# Citation
If you use the dataset please cite:
```
@inproceedings{acronym2020,
    title     = {{ACRONYM}: A Large-Scale Grasp Dataset Based on Simulation},
    author    = {Eppner, Clemens and Mousavian, Arsalan and Fox, Dieter},
    year      = {2020},
    booktitle = {Under Review at ICRA 2021}
}
```
