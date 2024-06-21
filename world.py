import numpy as np
import utils

from hit import Hit
from typing import List
from hittable import Hittable
from light import Light

class World:
    def __init__(self, hittables: List[Hittable], lights: List[Light]) -> None:
        # NOTE: maybe save camera object to get its center and calculate hit distance
        self.hittables = hittables
        self.lights = lights
        self.objects = self.hittables + self.lights

    def get_nearest_hit(self, ray) -> Hit | Light | None:
        nearest_hit = None

        for hittable in self.hittables + self.lights:
            current_hit: Hit | Light | None = hittable.intersects(ray)

            # If ray hitted object
            if current_hit != None:
                # Check if nearest_hit is defined yet
                if nearest_hit is None:
                    # If its not, than current is the nearest
                    nearest_hit = current_hit
                else:
                # If its defined already, then define nearest as current hit based on its distance to origin
                    current_hit_distance = 0.0

                    if isinstance(current_hit, Light):
                        current_hit_distance = utils.distance(current_hit.position, ray.origin)
                    elif isinstance(current_hit, Hit):
                        current_hit_distance = utils.distance(current_hit.point, ray.origin)
                    
                    if isinstance(nearest_hit, Light):
                        nearest_hit_distance = utils.distance(nearest_hit.position, ray.origin)
                    elif isinstance(nearest_hit, Hit):
                        nearest_hit_distance = utils.distance(nearest_hit.point, ray.origin)
                    
                    if current_hit_distance < nearest_hit_distance:
                        nearest_hit = current_hit
        
        return nearest_hit