import time

from hit import Hit
from typing import List
from hittable import Hittable
from light import Light

class World:
    def __init__(self, hittables: List[Hittable], lights: List[Light]) -> None:
        # NOTE: maybe save camera object to get its center and calculate hit distance
        self.hittables = hittables + lights
        self.lights = lights

    def get_nearest_hit(self, ray) -> Hit | None:
        neareast_hit = None

        for hittable in self.hittables:
            current_hit: Hit | None = hittable.intersects(ray)

            # If ray hitted object
            if current_hit != None:
                # Check if nearest_hit is defined yet
                if neareast_hit is None:
                    # If its not, than current is the nearest
                    neareast_hit = current_hit
                else:
                # If its defined already, then define nearest as current hit based on its distance to origin
                    if current_hit.distance_to_origin() < neareast_hit.distance_to_origin():
                        neareast_hit = current_hit
        
        return neareast_hit
