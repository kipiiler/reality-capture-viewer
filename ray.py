import numpy as np
import open3d as o3d
import open3d.visualization as vis

from renderer_utils import create_visualize_boundary_cube_with_anchor

class Ray:
    def __init__(self, origin, direction):
        self.origin = np.array(origin)
        self.direction = np.array(direction)

    def point_at_parameter(self, t):
        return self.origin + t * self.direction
    
    def __str__(self):
        return f"Ray(origin={self.origin}, direction={self.direction})"
    
    def get_geometry(self, length = 50.0):
        points = np.array([self.origin, self.origin + self.direction * length])
        lines = np.array([[0, 1]])
        colors = np.array([[1, 0, 0], [1, 0, 0]])
        line_set = o3d.geometry.LineSet(
            points=o3d.utility.Vector3dVector(points),
            lines=o3d.utility.Vector2iVector(lines)
        )
        line_set.colors = o3d.utility.Vector3dVector(colors)
        return line_set
    

class HitRecord:
    def __init__(self, t, p, normal):
        self.t = t
        self.p = p
        self.normal = normal

    def __str__(self):
        return f"HitRecord(t={self.t}, p={self.p}, normal={self.normal})"
    

class Hittable:
    def hit(self, ray, t_min, t_max):
        raise NotImplementedError("hit method not implemented")
    

class Cube(Hittable):
    def __init__(self, center, side_length):
        self.center = np.array(center)
        self.side_length = side_length

    def hit(self, ray, t_min: float, t_max: float):
        half_side = self.side_length / 2
        t_min = t_min
        t_max = t_max
        t_values = []

        for i in range(3):
            if ray.direction[i] == 0:
                if ray.origin[i] < self.center[i] - half_side or ray.origin[i] > self.center[i] + half_side:
                    return None
            else:
                t1 = (self.center[i] - half_side - ray.origin[i]) / ray.direction[i]
                t2 = (self.center[i] + half_side - ray.origin[i]) / ray.direction[i]
                t_min = max(t_min, min(t1, t2))
                t_max = min(t_max, max(t1, t2))
                t_values.append((t_min, t_max))

        if t_values[0][0] > t_values[0][1] or t_values[1][0] > t_values[1][1] or t_values[2][0] > t_values[2][1]:
            return None
        
        t_min = max(t_values[0][0], t_values[1][0], t_values[2][0])
        t_max = min(t_values[0][1], t_values[1][1], t_values[2][1])

        if t_min > t_max:
            return None
        
        t = t_min
        p = ray.point_at_parameter(t)
        normal = np.zeros(3)

        for i in range(3):
            if p[i] < self.center[i] - half_side + 1e-6:
                normal[i] = -1
            elif p[i] > self.center[i] + half_side - 1e-6:
                normal[i] = 1

        return HitRecord(t, p, normal)
    
    def get_geometry(self):
        lower_left = self.center - self.side_length / 2
        print(lower_left)

        return create_visualize_boundary_cube_with_anchor(self.side_length, lower_left, color=[1., 0., 0.])
