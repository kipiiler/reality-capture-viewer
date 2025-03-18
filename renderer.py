import open3d as o3d
import numpy as np
import copy
from transform import convert_coordinate_system_pcd, prune_point_cloud_cube


class Renderer:
    def __init__(self):
        self.source_pcd = o3d.geometry.PointCloud()
        self.added_pcd = []
        self.pcd_ids = {}
        self.current_pcd_id = 0
        self.vis = o3d.visualization.VisualizerWithKeyCallback()

    def load_source_pcd(self, pcd_path, convert_coord=True, max_distance=None):
        self.source_pcd = o3d.io.read_point_cloud(pcd_path)
        if convert_coord:
            self.source_pcd = convert_coordinate_system_pcd(self.source_pcd)
        if max_distance is not None:
            self.source_pcd = prune_point_cloud_cube(self.source_pcd, max_distance)

    def load_pcd_from_path(self, pcd_path, convert_coord=True):
        pcd = o3d.io.read_point_cloud(pcd_path)
        if convert_coord:
            pcd = convert_coordinate_system_pcd(pcd)

        self.added_pcd.append(pcd)
        self.current_pcd_id += 1
        self.pcd_ids[self.current_pcd_id] = pcd

    def load_pcd(self, pcd, convert_coord=False, custom_id=None):
        if convert_coord:
            pcd = convert_coordinate_system_pcd(pcd)

        if custom_id is not None and custom_id not in self.pcd_ids:
            self.pcd_ids[custom_id] = pcd
            self.added_pcd.append(pcd)
        else:
            self.added_pcd.append(pcd)
            self.current_pcd_id += 1
            self.pcd_ids[self.current_pcd_id] = pcd

    def access_pcd(self, pcd_id):
        if pcd_id in self.pcd_ids:
            return self.pcd_ids[pcd_id]
        else:
            print(f"Point cloud with ID {pcd_id} does not exist")
            return None

    def load_lineset(self, lineset):
        self.added_pcd.append(lineset)
        self.current_pcd_id += 1
        self.pcd_ids[self.current_pcd_id] = lineset
    
    def remove_pcd(self, pcd_id):
        if pcd_id in self.pcd_ids:
            self.added_pcd.remove(self.pcd_ids[pcd_id])
            del self.pcd_ids[pcd_id]
        else:
            print(f"Point cloud with ID {pcd_id} does not exist")

    def render(self, key_to_callback=None):

        self.vis.create_window()
        self.vis.add_geometry(self.source_pcd)
        for pcd in self.added_pcd:
            self.vis.add_geometry(pcd)

        if key_to_callback is not None:
            for key, callback in key_to_callback.items():
                self.vis.register_key_callback(key, callback)
        self.vis.run()
        self.vis.destroy_window()

    