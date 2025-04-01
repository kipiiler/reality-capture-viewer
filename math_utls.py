import numpy as np
import math

def extract_rotation_position_scale_uniform(matrix):
    """
    Extracts rotation, position, and uniform scale from a 4x4 transformation matrix.

    Args:
        matrix: A 4x4 numpy array representing the transformation matrix.

    Returns:
        A tuple containing:
            - rotation: A 3x3 numpy array representing the rotation matrix.
            - position: A 3x1 numpy array representing the position vector.
            - scale: A float representing the uniform scale factor.
    """

    matrix = np.array(matrix, dtype=float)

    position = matrix[:3, 3].reshape(3, 1)

    scale_x = np.linalg.norm(matrix[:3, 0])
    scale_y = np.linalg.norm(matrix[:3, 1])
    scale_z = np.linalg.norm(matrix[:3, 2])

    if not np.isclose(scale_x, scale_y) or not np.isclose(scale_x, scale_z) or not np.isclose(scale_y, scale_z):
        raise ValueError("Non-uniform scaling detected. This function only handles uniform scaling.")

    scale = scale_x

    rotation = matrix[:3, :3] / scale

    rotation_transpose = rotation.T
    identity = np.dot(rotation, rotation_transpose)
    if not np.allclose(identity, np.eye(3)):
        print("Warning: Rotation matrix is not perfectly orthogonal, there may be some shear or other transformations in the matrix")

    return rotation, position, scale

def rotation_matrix_to_euler_angles(rotation_matrix):
    """
    Converts a 3x3 rotation matrix to Euler angles (roll, pitch, yaw) in degrees.
    Roll: rotation around x-axis
    Pitch: rotation around y-axis
    Yaw: rotation around z-axis

    Args:
        rotation_matrix: A 3x3 numpy array representing the rotation matrix.

    Returns:
        A tuple (roll, pitch, yaw) in degrees.
    """
    sy = math.sqrt(rotation_matrix[0, 0] ** 2 + rotation_matrix[1, 0] ** 2)

    singular = sy < 1e-6

    if not singular:
        roll = math.atan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
        pitch = math.atan2(-rotation_matrix[2, 0], sy)
        yaw = math.atan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
    else:
        roll = math.atan2(-rotation_matrix[1, 2], rotation_matrix[1, 1])
        pitch = math.atan2(-rotation_matrix[2, 0], sy)
        yaw = 0

    return math.degrees(roll), math.degrees(pitch), math.degrees(yaw)
