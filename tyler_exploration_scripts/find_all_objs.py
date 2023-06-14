import os

# Print out the number of .obj files in each directory
# The models that passed watertight without error and those that are referenced in acronym
input_dir = "/juno/u/tylerlum/github_repos/acronym/data/ShapeNetSem_restructured/meshes/"
input_dir_2 = "/juno/u/tylerlum/github_repos/Manifold/WatertightShapeNetSem/models/"

filenames = []
for object_category in os.listdir(input_dir):
    for filename in os.listdir(os.path.join(input_dir, object_category)):
        if not filename.endswith(".obj"):
            continue
        filenames.append(filename)

filenames_2 = []
for filename in os.listdir(input_dir_2):
    if not filename.endswith(".obj"):
        continue
    filenames_2.append(filename)

filenames = set(filenames)
filenames_2 = set(filenames_2)

print(f"From {input_dir}: {len(filenames)}")
print(f"From {input_dir_2}: {len(filenames_2)}")

only_in_1 = filenames.difference(filenames_2)
only_in_2 = filenames_2.difference(filenames)
print(f"Only in {input_dir}: {len(only_in_1)}")
print(f"Only in {input_dir_2}: {len(only_in_2)}")

print(f"Examples in {input_dir} but not in {input_dir_2}: {list(only_in_1)[:10]}")