import numpy as np
import open3d as o3d

def euler_to_rotation_matrix(yaw, pitch, roll):
    """
    Compute rotation matrix based on RealityCapture's Yaw (Z), Pitch (Y), Roll (X).
    """
    # Convert degrees to radians
    print(yaw, pitch, roll)
    yaw, pitch, roll = np.radians([yaw, pitch, roll])
    print(yaw, pitch, roll)
    # Compute sines and cosines
    cx, cy, cz = np.cos([roll, pitch, yaw])
    sx, sy, sz = np.sin([roll, pitch, yaw])

    # RealityCapture-style rotation matrix
    R = np.array([
        [ cx * cz + sx * sy * sz, -cx * sz + cz * sx * sy, -cy * sx ],
        [-cy * sz,                -cy * cz,                -sy     ],
        [ cx * sy * sz - cz * sx,  cx * cz * sy + sx * sz, -cx * cy ]
    ])
    
    return R

def create_camera_transformation_matrix(position, rotation, use_custom_cal = False):
    heading, pitch, roll = rotation
    # Compute rotation matrix
    if use_custom_cal:
        rotation_matrix = euler_to_rotation_matrix(*rotation)
    else:
        rotation_matrix = o3d.geometry.get_rotation_matrix_from_zyx(
            [np.radians(heading), np.radians(pitch), np.radians(roll)]
        )

    # Create transformation matrix
    transformation = np.eye(4)
    transformation[:3, :3] = rotation_matrix
    transformation[:3, 3] = position

    # do a 180 degree rotation around the x axis
    # to convert from reality capture to open3d

    # transformation = np.dot(transformation, np.array([
    #     [1, 0, 0, 0],
    #     [0, -1, 0, 0],
    #     [0, 0, -1, 0],
    #     [0, 0, 0, 1]
    # ]))

    return transformation

def prune_point_cloud_cube(pcd, max_distance):
    """
    Prune points that are outside a cube centered at origin with side length 2*max_distance
    """
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors) if pcd.has_colors() else None
    
    # Find points within the cube (|x| <= max_distance, |y| <= max_distance, |z| <= max_distance)
    mask = np.logical_and.reduce((
        np.abs(points[:, 0]) <= max_distance,
        np.abs(points[:, 1]) <= max_distance,
        np.abs(points[:, 2]) <= max_distance
    ))
    
    # Create a new point cloud with only the points within the cube
    pruned_pcd = o3d.geometry.PointCloud()
    pruned_pcd.points = o3d.utility.Vector3dVector(points[mask])
    if colors is not None:
        pruned_pcd.colors = o3d.utility.Vector3dVector(colors[mask])
    
    return pruned_pcd

def convert_coordinate_system_pcd(pcd):
    # z 2 to y 1
    # y 1 to x 0
    # x 0 to z 2

    # convert from reality capture to open3d

    pcd_points = np.asarray(pcd.points)
    pcd_points[:,[0,1,2]] = pcd_points[:,[0,2,1]]
    pcd.points = o3d.utility.Vector3dVector(pcd_points)
    return pcd