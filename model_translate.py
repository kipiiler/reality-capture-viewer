import numpy as np
import open3d as o3d

from math_utls import extract_rotation_position_scale_uniform, rotation_matrix_to_euler_angles
from parser import read_camera_poses_from_file
from renderer import Renderer
from transform import create_camera_transformation_matrix
from plyfile import PlyData, PlyElement

def main():
    print("Loading transformation matrix...")
    matrix_file_path = "transformation_matrix.npy"
    matrix = np.load(matrix_file_path)

    print("Loading point cloud...")
    ply_file_path = "C:/Users/nguye/Desktop/3d/image_table_full/test.ply"
    renderer = Renderer()
    renderer.load_source_pcd(ply_file_path, max_distance=50)

    renderer.source_pcd.transform(matrix)

    print("Saving transformed point cloud...")
    o3d.io.write_point_cloud("transformed.ply", renderer.source_pcd)

    transformed_vertices = np.asarray(renderer.source_pcd.points)
    colors = np.asarray(renderer.source_pcd.colors) * 255.0 if renderer.source_pcd.has_colors() else None

    vertex_data = []
    for i in range(len(transformed_vertices)):
        x, y, z = transformed_vertices[i].astype(np.float32)
        if colors is not None:
            r, g, b = colors[i].astype(np.uint8)
            vertex_data.append((x, y, z, r, g, b))
        else:
            vertex_data.append((x, y, z))

    if colors is not None:
        vertex_dtype = [('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
                        ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')]
    else:
        vertex_dtype = [('x', 'f4'), ('y', 'f4'), ('z', 'f4')]

    # Create PlyElement and PlyData
    vertex_array = np.array(vertex_data, dtype=vertex_dtype)
    vertex_element = PlyElement.describe(vertex_array, 'vertex')
    plydata = PlyData([vertex_element], text=False)

    # Save with float precision
    plydata.write("transformed_with_float32.ply")
    print("Done! Output saved with float precision as transformed_with_float32.ply")

    print("Loading camera data...")
    camera_reg_path = "C:/Users/nguye/Desktop/3d/image_table_full/reg.csv"
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
        f.write("#name,x,y,alt,heading,pitch,roll,f,px,py,k1,k2,k3,k4,t1,t2\n")
        for filename, position, rotation in output_data:
            x, y, z = position.flatten()
            pitch, roll, heading = rotation
            f.write(f"{filename},{x},{y},{z},{heading},{pitch},{roll},30,0,0,0,0,0,0,0,0\n")        

if __name__ == "__main__":
    main()