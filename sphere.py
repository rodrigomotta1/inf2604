import numpy as np
import math

from ray import Ray
from hit import Hit

class Sphere:
    """
    Sphere surface abstraction class
    Intended to be used together with hittable objects, lights, etc..
    """
    def __init__(self, radius:float, center:np.ndarray) -> None:
        self.radius = radius
        self.center = center
    
    def __repr__(self) -> str:
        return f"[Sphere] center={self.center} radius={self.radius}"
    
    def intersects(self, ray:Ray) -> None | Hit | bool:
        """
        Checks if given ray intersects with self defined surface
        Returns None if no hit is detected
        Returns a Hit object with hit information if its detected
        """
        oc:np.ndarray = self.center - ray.origin
        normalized_dir:float = float(np.linalg.norm(ray.direction))
        a:float = np.dot(ray.direction, ray.direction)
        b:float = -2.0 * np.dot(ray.direction, oc)
        c:float = np.dot(oc, oc) - self.radius * self.radius
        delta:float = b * b - 4 * a * c

        if delta < 0:
            return None
        else:
            # sqrt_delta:float = math.sqrt(delta)

            return True
