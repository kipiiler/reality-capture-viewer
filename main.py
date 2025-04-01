from renderer import Renderer
from renderer_utils import create_camera_frustum_open3d, create_positive_axes
from input import key_to_callback
from parser import read_camera_poses_from_file
from transform import create_camera_transformation_matrix

def main():
    renderer = Renderer()
    renderer.load_source_pcd("transformed_with_float32.ply", convert_coord=False, max_distance=50)

    axes = create_positive_axes(50.0) # 5m 
    renderer.load_lineset(axes)
    renderer.load_wireframe_chunk(max_distance=20)

    camera_data = read_camera_poses_from_file("new_camera_data.csv", False)

    for i, (_, position, rotation) in enumerate(camera_data):
        print(f"Loading camera {i+1}/{len(camera_data)}")

        # Load camera point cloud
        camera = create_camera_frustum_open3d(scale=0.3)
        transformation = create_camera_transformation_matrix(position, rotation)
        camera.transform(transformation)
        renderer.load_pcd(camera, custom_id=f"camera_{i}")

    print("Rendering...")
    renderer.render(key_to_callback=key_to_callback)
    print("Done!")

if __name__ == "__main__":
    main()