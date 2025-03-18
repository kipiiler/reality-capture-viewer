import numpy as np
from renderer import Renderer
from renderer_utils import create_camera_frustum_open3d, create_positive_axes
from input import key_to_callback
from parser import read_camera_poses_from_file
from transform import create_camera_transformation_matrix

# Global transformation matrix
transformation_matrix = np.eye(4)

def apply_transformation(vis, pcds, transform):
    global transformation_matrix
    transformation_matrix = transform @ transformation_matrix
    for pcd in pcds:
        pcd.transform(transform)
        vis.update_geometry(pcd)
    return False

def translate_pcd(vis, pcds, delta):
    translation = np.eye(4)
    translation[:3, 3] = delta
    return apply_transformation(vis, pcds, translation)

def rotate_pcd(vis, pcds, axis, angle_deg):
    angle = np.radians(angle_deg)
    c, s = np.cos(angle), np.sin(angle)
    if axis == 'x':
        rot = np.array([
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1]
        ])
    elif axis == 'y':
        rot = np.array([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ])
    else:  # axis == 'z'
        rot = np.array([
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
    return apply_transformation(vis, pcds, rot)

def main():
    renderer = Renderer()
    renderer.load_source_pcd("C:/Users/nguye/Desktop/3d/test_data/test.ply", max_distance=50)

    axes = create_positive_axes(50.0)
    renderer.load_pcd(axes, custom_id="axes")

    camera_data = read_camera_poses_from_file("C:/Users/nguye/Desktop/3d/test_data/reg.csv", True)

    for i, (_, position, rotation) in enumerate(camera_data):
        camera = create_camera_frustum_open3d()
        transformation = create_camera_transformation_matrix(position, rotation)
        camera.transform(transformation)
        renderer.load_pcd(camera, custom_id=f"camera_{i}")

    list_models = [renderer.source_pcd]
    for key in renderer.pcd_ids:
        if key != "axes":
            list_models.append(renderer.pcd_ids[key])

    for model in list_models:
        model.transform(transformation_matrix)

    key_to_callback[ord("A")] = lambda vis: translate_pcd(vis, list_models, [-0.1, 0, 0])
    key_to_callback[ord("D")] = lambda vis: translate_pcd(vis, list_models, [0.1, 0, 0])
    key_to_callback[ord("W")] = lambda vis: translate_pcd(vis, list_models, [0, 0.1, 0])
    key_to_callback[ord("S")] = lambda vis: translate_pcd(vis, list_models, [0, -0.1, 0])
    key_to_callback[ord("Q")] = lambda vis: translate_pcd(vis, list_models, [0, 0, -0.1])
    key_to_callback[ord("E")] = lambda vis: translate_pcd(vis, list_models, [0, 0, 0.1])

    key_to_callback[ord("J")] = lambda vis: rotate_pcd(vis, list_models, 'x', -5)
    key_to_callback[ord("L")] = lambda vis: rotate_pcd(vis, list_models, 'x', 5)
    key_to_callback[ord("I")] = lambda vis: rotate_pcd(vis, list_models, 'y', 5)
    key_to_callback[ord("K")] = lambda vis: rotate_pcd(vis, list_models, 'y', -5)
    key_to_callback[ord("U")] = lambda vis: rotate_pcd(vis, list_models, 'z', -5)
    key_to_callback[ord("O")] = lambda vis: rotate_pcd(vis, list_models, 'z', 5)

    print("Rendering...")
    renderer.render(key_to_callback=key_to_callback)
    print("Done!")

    print("Final transformation matrix:")
    print(transformation_matrix)

if __name__ == "__main__":
    main()