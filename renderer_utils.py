import open3d as o3d
import numpy as np

def create_positive_axes(scale):
    points = [
        [0, 0, 0],
        [scale, 0, 0],
        [0, scale, 0],
        [0, 0, scale],
    ]
    lines = [
        [0, 1],
        [0, 2],
        [0, 3]
    ]
    colors = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]
    line_set = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(points),
        lines=o3d.utility.Vector2iVector(lines),
    )
    line_set.colors = o3d.utility.Vector3dVector(colors)
    return line_set

def create_infinite_axes():
    """
    Creates a set of long lines along the X, Y, and Z axes to simulate infinite axes.
    """
    # Define start and end points for each axis (very long lines)
    length = 100  # Large number to simulate infinite axes
    points = np.array([
        [-length, 0, 0], [length, 0, 0],  # X-axis (red)
        [0, -length, 0], [0, length, 0],  # Y-axis (green)
        [0, 0, -length], [0, 0, length]   # Z-axis (blue)
    ])
    
    # Define line connections (pairs of points)
    lines = [[0, 1], [2, 3], [4, 5]]
    
    # Define colors: Red for X, Green for Y, Blue for Z
    colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    # Create LineSet
    axis_lines = o3d.geometry.LineSet()
    axis_lines.points = o3d.utility.Vector3dVector(points)
    axis_lines.lines = o3d.utility.Vector2iVector(lines)
    axis_lines.colors = o3d.utility.Vector3dVector(colors)

    return axis_lines

def create_camera_frustum(fov_degrees=60, aspect_ratio=1.5, scale=1.0):
    """
    Creates a 3D frustum representation of the camera's field of view.

    Parameters:
    - fov_degrees: Field of View (FoV) in degrees
    - aspect_ratio: Aspect ratio (width/height)
    - scale: Frustum size scaling factor

    Returns:
    - Open3D frustum visualization as a LineSet object
    """
    import math

    # Convert FoV to radians
    fov_radians = math.radians(fov_degrees / 2.0)

    # Define frustum corners (near plane)
    near = scale
    far = scale * 2
    h = math.tan(fov_radians) * near
    w = h * aspect_ratio

    # Frustum vertices
    vertices = [
        [0, 0, 0],  # Camera center (apex)
        [-w, -h, -near], [w, -h, -near], [w, h, -near], [-w, h, -near],  # Near plane
        [-w * 2, -h * 2, -far], [w * 2, -h * 2, -far], [w * 2, h * 2, -far], [-w * 2, h * 2, -far]  # Far plane
    ]

    # Frustum edges
    edges = [
        (0, 1), (0, 2), (0, 3), (0, 4),  # Apex to near plane
        (1, 2), (2, 3), (3, 4), (4, 1),  # Near plane edges
        (1, 5), (2, 6), (3, 7), (4, 8),  # Near to far connections
        (5, 6), (6, 7), (7, 8), (8, 5)   # Far plane edges
    ]

    # Create Open3D LineSet
    frustum = o3d.geometry.LineSet()
    frustum.points = o3d.utility.Vector3dVector(vertices)
    frustum.lines = o3d.utility.Vector2iVector(edges)

    return frustum

def create_camera_frustum_open3d(scale=1.0):
    camera = o3d.geometry.LineSet.create_camera_visualization(
        intrinsic=o3d.camera.PinholeCameraIntrinsic(
            o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault
        ),
        extrinsic=np.eye(4),
        scale=scale
    )
    return camera

def create_visualize_boundary_cube(length, origin):
    """
    Create a wireframe cube to visualize the boundary, with given length and
    original as lower-left corner
    """

    points = [
        origin,  # 0
        [origin[0] + length, origin[1], origin[2]],  # 1
        [origin[0], origin[1] + length, origin[2]],  # 2
        [origin[0] + length, origin[1] + length, origin[2]],  # 3
        [origin[0], origin[1], origin[2] + length],  # 4
        [origin[0] + length, origin[1], origin[2] + length],  # 5
        [origin[0], origin[1] + length, origin[2] + length],  # 6
        [origin[0] + length, origin[1] + length, origin[2] + length]  # 7
    ]

    lines = [
        [0, 1], [0, 2], [0, 4],  # bottom face
        [1, 3], [1, 5], [2, 3],  # bottom face
        [2, 6], [3, 7], [4, 5],  # bottom face
        [4, 6], [5, 7], [6, 7]   # bottom face
    ]

    colors = [[0.8, 0.8, 0.8] for _ in range(len(lines))]

    line_set = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(points),
        lines=o3d.utility.Vector2iVector(lines)
    )

    line_set.colors = o3d.utility.Vector3dVector(colors)
    return line_set

def create_visualize_boundary_cube(max_distance):
    """
    Create a wireframe cube to visualize the boundary
    """
    lower_left = [-max_distance, -max_distance, -max_distance]
    return create_visualize_boundary_cube(max_distance, lower_left)