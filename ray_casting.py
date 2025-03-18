from ray import Ray
from renderer import Renderer
from renderer_utils import create_camera_frustum_open3d, create_positive_axes
from input import key_to_callback
from parser import process_camera_mapping, read_camera_poses_from_file, write_chunk_map_to_file
from transform import create_camera_transformation_matrix

ply_file_path = "data/transformed.ply"
camera_file_path = "data/new_camera_data.csv"
transformed = True

CHUNK_SIZE = 10.0
MAX_DISTANCE = 50.0

ray_index = 0
def update_ray_index(vis, camera_geos, idx):
    global ray_index
    prev_index = ray_index
    prev_data = camera_geos[prev_index]

    ray_index = idx % len(camera_geos)
    data = camera_geos[ray_index]

    ctr = vis.get_view_control()
    prev_params = ctr.convert_to_pinhole_camera_parameters()


    print(f"Switching to camera {ray_index}")
    vis.remove_geometry(prev_data["cam"])
    vis.remove_geometry(prev_data["ray"])
    for cube in prev_data["hit_cubes"]:
        vis.remove_geometry(cube)

    vis.add_geometry(data["cam"])
    vis.add_geometry(data["ray"])
    for cube in data["hit_cubes"]:
        vis.add_geometry(cube)
    
    vis.update_renderer()
    ctr.convert_from_pinhole_camera_parameters(prev_params)

    print(f"Switched to camera {ray_index}")
    return False


def main():
    renderer = Renderer()

    renderer.load_source_pcd(ply_file_path, convert_coord=False, max_distance=50)

    axes = create_positive_axes(50.0) # 5m 
    renderer.load_lineset(axes)
    renderer.load_wireframe_chunk(max_distance=MAX_DISTANCE)
    cubes = renderer.generate_chunk_cube(max_distance=MAX_DISTANCE)

    camera_data = read_camera_poses_from_file(camera_file_path, False)

    camera_geos = []
    for i, (frame, position, rotation) in enumerate(camera_data):
        print(f"Loading camera {i+1}/{len(camera_data)}")

        # Load camera point cloud
        camera = create_camera_frustum_open3d(scale=0.3)
        transformation = create_camera_transformation_matrix(position, rotation)
        camera.transform(transformation)
        # renderer.load_pcd(camera, custom_id=f"camera_{i}")

    # camera = renderer.access_pcd("camera_7")
        ray_origin = position
        ray_direction = transformation[:3, 2]  # Assuming the camera's forward direction is the third column of the rotation matrix
        ray = Ray(ray_origin, ray_direction)
        ray_line = ray.get_geometry(100.0)

        cube_hit = []
        cube_centers = []
        for cube in cubes:
            hit_record = cube.hit(ray, 0.0, 1000.0)
            if hit_record is not None:
                cube_geometry = cube.get_geometry()
                cube_hit.append(cube_geometry)
                cube_centers.append(cube.center)

        camera_geos.append({
            "id": f"camera_{i}",
            "cam": camera,
            "position": position,
            "rotation": rotation,
            "hit_cubes": cube_hit,
            "hit_cube_centers": cube_centers,
            "ray": ray_line,
            "frame": frame
        })

    key_to_callback[ord("A")] = lambda vis: update_ray_index(vis, camera_geos, ray_index + 1)
    key_to_callback[ord("D")] = lambda vis: update_ray_index(vis, camera_geos, ray_index - 1)

    print("Rendering...")
    renderer.render(key_to_callback=key_to_callback)
    print("Done!")
    chunk_map = process_camera_mapping(camera_geos, CHUNK_SIZE, MAX_DISTANCE)
    print(f"Chunk map created with {len(chunk_map)} chunks")
    write_chunk_map_to_file("chunk_map.json", chunk_map)


if __name__ == "__main__":
    main()