import re
import os

MODELS_DIR = 'data/ShapeNetSem/models'

def get_jpg_files_from_mtl(mtl_file):
    jpg_files = []
    with open(os.path.join(MODELS_DIR, mtl_file), 'r') as f:
        mtl_data = f.read()
        matches = re.findall(r"map_K[ad]\s(.+\.jpg)", mtl_data)
        for match in matches:
            jpg_files.append(match)
    return jpg_files


for filename in os.listdir(MODELS_DIR):
    if filename.endswith('.obj'):
        continue
    jpg_files = get_jpg_files_from_mtl(filename)
    print(f"{filename} => {jpg_files}")
    if len(jpg_files) == 0:
        print("===================")
        print(f"WARNING: {len(jpg_files)}")
        print("===================")
