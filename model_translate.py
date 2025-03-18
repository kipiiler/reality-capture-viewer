import numpy as np
import open3d as o3d

from math_utls import extract_rotation_position_scale_uniform, rotation_matrix_to_euler_angles
from parser import read_camera_poses_from_file
from renderer import Renderer
from transform import create_camera_transformation_matrix

def main():
    print("Loading transformation matrix...")
    matrix_file_path = "transformation_matrix.npy"
    matrix = np.load(matrix_file_path)

    print("Loading point cloud...")
    ply_file_path = "C:/Users/nguye/Desktop/3d/test_data/test.ply"
    renderer = Renderer()
    renderer.load_source_pcd(ply_file_path, max_distance=50)

    renderer.source_pcd.transform(matrix)

    print("Saving transformed point cloud...")
    o3d.io.write_point_cloud("transformed.ply", renderer.source_pcd)

    print("Loading camera data...")
    camera_reg_path = "C:/Users/nguye/Desktop/3d/test_data/reg.csv"
    camera_data = read_camera_poses_from_file(camera_reg_path, True)

    output_data = []
    for i, (filename, position, rotation) in enumerate(camera_data):
        print(f"Loading camera {i+1}/{len(camera_data)}")

        print(f"Position for camera {i+1}: {position}")
        print(f"Rotation for camera {i+1}: {rotation}")

        # Load camera point cloud
        transformation = create_camera_transformation_matrix(position, rotation)
        final_matrix = matrix @ transformation

        new_pos = final_matrix[:3, 3]
        print(f"New position for camera {i+1}: {new_pos}")

        rot_mat, _, _ = extract_rotation_position_scale_uniform(final_matrix)
        new_rot = rotation_matrix_to_euler_angles(rot_mat)
        print(f"New rotation for camera {i+1}: {new_rot}")
        output_data.append((filename, new_pos, new_rot))

    print("Saving new camera data...")
    with open("new_camera_data.csv", "w") as f:
        f.write("#name,position,rotation\n")
        for filename, position, rotation in output_data:
            x, y, z = position.flatten()
            heading, pitch, roll = rotation
            f.write(f"{filename},{x},{y},{z},{heading},{pitch},{roll}\n")        

if __name__ == "__main__":
    main()