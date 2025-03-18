import numpy as np

def parse_line(line, convert_coord = True):
    line = line.strip().split(",")
    filename = line[0]
    position = np.array([float(x) for x in line[1:4]])
    rotation = np.array([float(x) for x in line[4:7]])
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