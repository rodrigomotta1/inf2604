import numpy as np
import utils
import math

from ray import Ray
from hit import Hit
from utils import HIT_TOLERANCE, normalize

class Box:
    def __init__(self, min_corner: np.ndarray, max_corner: np.ndarray, ) -> None:
        self.min_corner = min_corner
        self.max_corner = max_corner

        self.transform = np.eye(4) # Base transformation matrix

    def intersects(self, hittable: object, ray: Ray) -> Hit | None:
        """
        Checks intersection between given ray and self object.
        Ray are transformed inside here to check intersection between ray ant transformed self object
        """
    
        # Apply current transformation within this object over given ray
        inv_transform:np.ndarray = np.linalg.inv(self.transform)
        transformed_ray:Ray = ray.transform(inv_transform)

        t0:np.ndarray = (self.min_corner - transformed_ray.origin) / transformed_ray.direction
        t1:np.ndarray = (self.max_corner - transformed_ray.origin) / transformed_ray.direction

        t_near:np.ndarray = np.minimum(t0, t1)
        t_far:np.ndarray = np.maximum(t0, t1) 

        t_min:float = np.max(t_near)
        t_max:float = np.min(t_far)

        if t_min > t_max or t_max < 0:
            return None
        
        t_hit:float = t_min if t_min > 0 else t_max
        local_hit_point:np.ndarray = transformed_ray.at(t_hit)
        local_normal:np.ndarray = self._calculate_normal(local_hit_point)

        world_hit_point:np.ndarray = self.transform @ np.append(local_hit_point, 1.0)
        world_normal:np.ndarray = np.linalg.inv(self.transform[:3, :3]).T @ local_normal

        is_backface:bool = np.dot(ray.direction, world_normal) > 0
        world_normal = -world_normal if is_backface else world_normal

        return Hit(world_hit_point[:3], world_normal, is_backface, instance=hittable, t=t_hit)

    def _calculate_normal(self, point:np.ndarray) -> np.ndarray:
        """
        Auxiliary method to evaluate normal at given box point
        """
        center = (self.min_corner + self.max_corner) * 0.5
        extent = (self.max_corner - self.min_corner) * 0.5

        local_hit_point = (point - center) / extent

        if abs(local_hit_point[0]) > 1 - utils.HIT_TOLERANCE:
            return np.array([np.sign(local_hit_point[0]), 0, 0])
        
        elif abs(local_hit_point[1]) > 1 - utils.HIT_TOLERANCE:
            return np.array([0, np.sign(local_hit_point[1]), 0])
        
        elif abs(local_hit_point[2]) > 1 - utils.HIT_TOLERANCE:
            return np.array([0, 0, np.sign(local_hit_point[2])])
        
        else:
            return np.array([0, 0, 0])
    
    def translate(self, translation: np.ndarray) -> 'Box':
        translation_matrix = np.eye(4)
        translation_matrix[:3, 3] = translation
        self.transform = translation_matrix @ self.transform

        return self

    def rotate(self, angle: float, axis: np.ndarray) -> 'Box':
        axis = utils.normalize(axis)
        cos_angle = np.cos(np.radians(angle))
        sin_angle = np.sin(np.radians(angle))
        ux, uy, uz = axis

        rotation_matrix = np.array([
            [cos_angle + ux**2 * (1 - cos_angle), ux * uy * (1 - cos_angle) - uz * sin_angle, ux * uz * (1 - cos_angle) + uy * sin_angle, 0],
            [uy * ux * (1 - cos_angle) + uz * sin_angle, cos_angle + uy**2 * (1 - cos_angle), uy * uz * (1 - cos_angle) - ux * sin_angle, 0],
            [uz * ux * (1 - cos_angle) - uy * sin_angle, uz * uy * (1 - cos_angle) + ux * sin_angle, cos_angle + uz**2 * (1 - cos_angle), 0],
            [0, 0, 0, 1]
        ])

        self.transform = rotation_matrix @ self.transform

        return self
    
    def apply_transform(self) -> None:
        # Transform the corners of the box
        corners = [
            self.min_corner,
            [self.min_corner[0], self.min_corner[1], self.max_corner[2]],
            [self.min_corner[0], self.max_corner[1], self.min_corner[2]],
            [self.min_corner[0], self.max_corner[1], self.max_corner[2]],
            [self.max_corner[0], self.min_corner[1], self.min_corner[2]],
            [self.max_corner[0], self.min_corner[1], self.max_corner[2]],
            [self.max_corner[0], self.max_corner[1], self.min_corner[2]],
            self.max_corner
        ]

        transformed_corners = []
        for corner in corners:
            transformed_corner = self.transform @ np.append(corner, 1)
            transformed_corners.append(transformed_corner[:3])

        transformed_corners = np.array(transformed_corners)

        self.min_corner = np.min(transformed_corners, axis=0)
        self.max_corner = np.max(transformed_corners, axis=0)

        self.transform = np.eye(4)  # Reset transform matrix

# # Criação de uma caixa
# min_corner = np.array([-1.0, -1.0, -1.0])
# max_corner = np.array([1.0, 1.0, 1.0])
# box = Box(min_corner, max_corner)

# # Aplicando transformações encadeadas
# box.translate(np.array([2.0, 3.0, 1.0])).rotate(45, np.array([0.0, 1.0, 0.0]))

# # Criação de um raio
# origin = np.array([0.0, 0.0, 0.0])
# direction = np.array([1.0, 1.0, 1.0])
# ray = Ray(origin, direction)

# # Checando interseção
# hit = box.intersects(box, ray)

# if hit:
#     print(f"Interseção detectada em {hit.point} com a normal {hit.normal}")
#     print(f"Backface: {hit.backface}")
# else:
#     print("Nenhuma interseção detectada")