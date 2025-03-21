import numpy as np
import json

def parse_line(line, convert_coord = True):
    line = line.strip().split(",")
    filename = line[0]
    position = np.array([float(x) for x in line[1:4]])
    rotation = np.array([float(x) for x in line[4:7]])
    # f = line[7]
    # px = line[8]
    # py = line[9]
    # k1 = line[10]
    # k2 = line[11]
    # k3 = line[12]
    # k4 = line[13]
    if convert_coord:
        position = np.array([position[0], position[2], position[1]])
    return filename, position, rotation


def read_camera_poses_from_file(filename, convert_coord = True):
    """
    Read camera poses from a text file.
    
    Each line should contain the following information:
    - Filename: Image filename
    - Position: (x, y, z) in world coordinates
    - Rotation: (omega, phi, kappa) in degrees
    
    Returns:
    - List of tuples (filename, position, rotation)
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    camera_poses = []
    for line in lines:
        if("#name" in line):
            continue
        filename, position, rotation = parse_line(line, convert_coord)
        camera_poses.append((filename, position, rotation))
    
    return camera_poses

def export_camera_pose_to_file(filename, camera_poses):
    """
    Export camera poses to a text file.
    
    Each line should contain the following information:
    - Filename: Image filename
    - Position: (x, y, z) in world coordinates
    - Rotation: (omega, phi, kappa) in degrees
    """
    with open(filename, 'w') as f:
        for filename, position, rotation in camera_poses:
            f.write(f"{filename},{position[0]},{position[1]},{position[2]},{rotation[0]},{rotation[1]},{rotation[2]}\n")


def process_camera_mapping(camera_geos, chunk_size: float, max_distance: float):
    
    top_left = [max_distance, max_distance, max_distance]
    bottom_right = [-max_distance, -max_distance, -max_distance]

    chunk_map = {}
    for x in range(int(bottom_right[0]), int(top_left[0]), int(chunk_size)):
        for y in range(int(bottom_right[1]), int(top_left[1]), int(chunk_size)):
            for z in range(int(bottom_right[2]), int(top_left[2]), int(chunk_size)):
                chunk_map[f"chunk_{x}_{y}_{z}"] = []

    ###
    #  camera_data:
    #   position: [x, y, z]
    #   rotation: [heading, pitch, roll]
    #   frame: str
    ###

    for i, camera_data in enumerate(camera_geos):
        position = camera_data["position"].tolist()
        rotation = camera_data["rotation"].tolist()
        frame = camera_data["frame"]        
        for c in camera_data["hit_cube_centers"]:
            x, y, z = c - chunk_size / 2
            chunk_map[f"chunk_{int(x)}_{int(y)}_{int(z)}"].append((frame, position, rotation))

    return chunk_map

def write_chunk_map_to_file(filename, chunk_map):
    with open(filename, 'w') as f:
        json.dump(chunk_map, f, indent=4)