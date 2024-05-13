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
    
    def get_nearest_light_hit(self, ray, light):
        """
        Looks like nearest hit but checking only the hittable lights from self.light
        In this case, only checks if nearest hit is equal to recevied light instance.
        Returns true if hitted light is equal to given light

        """
        hits = []

        for light in self.lights:
            # Calculate light intersection
            # 0. Calculate light distance from ray origin as ray_to_light
            ray_to_light = utils.distance(ray.origin, light.position)

            # 1. Evaluate ray the r(t) with t=ray_to_light
            ray_at_calculated_dist = ray.at(ray_to_light)

            # 2. Check if r(t=ray_to_light) distance to light.position is within HIT_TOLERANCE interval
            distance_from_light = utils.distance(ray_at_calculated_dist, light.position)

            if distance_from_light <= utils.HIT_TOLERANCE:
                hits.append((light, distance_from_light))
        
        if len(hits) == 0:
            return False
        else:
            return min(hits, key=lambda x: x[1])[0] == light # Get minimum tuple comparing second entry of each and returing the first entry of minimum tuple