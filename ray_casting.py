    # renderer = Renderer()
    # ray_test = Ray([0, 0, 0], [1, 1, 1])

    # axes = create_positive_axes(50.0) # 5m
    # ray_line = ray_test.get_geometry(50.0)

    # cube_test = Cube([0., 5., 0.], 2)
    # cube = cube_test.get_geometry()

    # renderer.load_lineset(axes)
    # renderer.load_lineset(ray_line)
    # renderer.load_lineset(cube)

    # cube_test.hit(ray_test, 0.0, 1000.0)
    # print(cube_test.hit(ray_test, 0.0, 1000.0))

    # renderer.render(key_to_callback=key_to_callback)
    # print("Done!")

from renderer import Renderer
from renderer_utils import create_camera_frustum_open3d, create_positive_axes
from input import key_to_callback
from parser import read_camera_poses_from_file
from transform import create_camera_transformation_matrix

ply_file_path = "data/transformed.ply"
camera_file_path = "data/new_camera_data.csv"
transformed = True

def main():
    renderer = Renderer()
    renderer.load_source_pcd(ply_file_path, convert_coord=False, max_distance=50)

    axes = create_positive_axes(50.0) # 5m 
    renderer.load_lineset(axes)
    renderer.load_wireframe_chunk(max_distance=20)

    camera_data = read_camera_poses_from_file(camera_file_path, False)

    for i, (_, position, rotation) in enumerate(camera_data):
        # if i == 45:
        print(f"Loading camera {i+1}/{len(camera_data)}")

        # Load camera point cloud
        camera = create_camera_frustum_open3d(scale=0.3)
        transformation = create_camera_transformation_matrix(position, rotation)
        camera.transform(transformation)
        renderer.load_pcd(camera, custom_id=f"camera_{i}")

    # camera = renderer.access_pcd("camera_7")

    print("Rendering...")
    renderer.render(key_to_callback=key_to_callback)
    print("Done!")

if __name__ == "__main__":
    main()