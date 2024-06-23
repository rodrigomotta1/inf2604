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

            if current_hit != None:
                if nearest_hit is None:
                    nearest_hit = current_hit
                else:
                    if utils.distance(current_hit.position, ray.origin) < utils.distance(nearest_hit.position, ray.origin):
                        nearest_hit = current_hit
        
        return nearest_hit