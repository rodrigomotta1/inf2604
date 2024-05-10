import numpy as np

from ray import Ray
from hit import Hit
from utils import HIT_TOLERANCE, normalize

class Plane:
    def __init__(self, point:np.ndarray, normal:np.ndarray) -> None:
        self.point = point
        self.normal = normalize(normal)
        self.raw_normal = normal

    def __repr__(self) -> str:
        return f"[Plane] point={self.point} normal={self.normal}"
    
    def intersects(self, ray:Ray) -> None | Hit:
        denominator:float = np.dot(ray.direction, self.normal)

        if np.abs(denominator) < HIT_TOLERANCE:
            return None
        else:
            ray_plane_point = ray.origin - self.point

            root:float = np.dot(ray_plane_point, self.normal) / denominator

            if root < 0:
                # Plane intersection is behind camera
                return None

            point:np.ndarray = ray.at(root)
            is_backface:bool = np.dot(ray.direction, self.normal) > 0
            # distance_to_eye = float(np.linalg.norm(point - ray.origin)) # TODO: CHECK THIS IF ANY ERROR

            return Hit(point, self.normal, is_backface)