import numpy as np
import math
import time

from ray import Ray
from hit import Hit
from utils import HIT_TOLERANCE, normalize

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
    
    def intersects(self, hittable:object, ray:Ray) -> None | Hit:
        """
        Checks if given ray intersects with self defined surface
        Returns None if no hit is detected
        Returns a Hit object with hit information if its detected
        """
        # TODO: Check how to accept roots in a given interval HIT_TOLERANCE

        oc:     np.ndarray  = self.center - ray.origin
        a:      float       = np.dot(ray.direction, ray.direction)
        b:      float       = -2 * np.dot(ray.direction, oc)
        c:      float       = np.dot(oc, oc) - self.radius * self.radius
        delta:  float       = b * b - 4 * a * c

        # If no real root, no hit
        if delta < 0:
            return None
        else:
            # NOTE: The first hit of ray into the surface is always the lesser positive root value (in this specific case) -> need to be checked in the future
            root_min:float = (-b - math.sqrt(delta)) / (2.0 * a)
            root_max:float = (-b + math.sqrt(delta)) / (2.0 * a)

            if root_max < HIT_TOLERANCE and root_min < HIT_TOLERANCE:
                return None
            
            root = min(root_min, root_max) if root_min > HIT_TOLERANCE else root_max
            if root < HIT_TOLERANCE:
                return None
            

            # NOTE: Always draw the normal outwards surfaces!
            hit_point:      np.ndarray      = ray.at(root)  
            normal_at_hit:  np.ndarray      = normalize((hit_point - self.center) / self.radius)
            is_backface:    bool            = np.dot(ray.direction, normal_at_hit) < 0

            
            return Hit(
                point=hit_point,
                normal=normal_at_hit,
                backface=is_backface,
                instance=hittable,
                t=root_min
            )

        


        
