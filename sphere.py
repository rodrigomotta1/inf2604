import numpy as np
import math

from ray import Ray
from hit import Hit
from utils import EPSILON, normalize

class Sphere:
    """
    Sphere surface abstraction class
    Intended to be used together with hittable objects, lights, etc..
    """
    def __init__(self, center:np.ndarray, radius:float,) -> None:
        self.radius = radius
        self.center = center
    
    def __repr__(self) -> str:
        return f"[Sphere] center={self.center} radius={self.radius}"
    
    def intersects(self, ray:Ray) -> None | Hit:
        """
        Checks if given ray intersects with self defined surface
        Returns None if no hit is detected
        Returns a Hit object with hit information if its detected
        """
        # print(f"self.center={self.center} ray.origin={ray.origin}")
        oc:np.ndarray = self.center - ray.origin
        a:float = np.dot(ray.direction, ray.direction)
        b:float = -2 * np.dot(ray.direction, oc)
        c:float = np.dot(oc, oc) - self.radius * self.radius
        delta:float = b * b - 4 * a * c

        # If no real root, no hit
        if delta < 0:
            return None

        root_min:float = (-b - math.sqrt(delta)) / (2.0 * a)
        root_max:float = (-b + math.sqrt(delta)) / (2.0 * a)

        hit_t:float = 0.0

        if root_min <= -EPSILON or root_min >= EPSILON:
            if root_max <= -EPSILON or root_max >= EPSILON:
                return None
            else:
                hit_t:float = root_max
        else:
            hit_t:float = root_min

        hit_point:np.ndarray = ray.at(hit_t)
        normal_at_hit:np.ndarray = normalize((hit_point - self.center) / self.radius)
        is_backface:bool = np.dot(ray.direction, normal_at_hit) < 0

        # NOTE: Always draw the normal outwards surfaces!

        return Hit(
            point=hit_point,
            normal=normal_at_hit,
            backface=is_backface
        )
