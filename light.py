import numpy as np
import utils
import color as colors

from ray import Ray
from hit import Hit
from typing import Tuple


class Light:
    """
    Point light source implementation
    # TODO: Implement other types of light sources
    """
    def __init__(self, position:np.ndarray, power:float, shape=None, color:np.ndarray = colors.WHITE) -> None:
        self.position = position
        self.power = power
        self.shape = shape
        self.color = color
    
    def radiance(self, world, hit:Hit) -> Tuple[float, np.ndarray]:
        """
        Calculates amount of light on given hit position.
        Traces auxiliary array to check if given hit position is in shadow, i.e., is obstructed by a hittable object before reaches light source

        Returns black if ray can't intersect this light source before any other hittable object or light source
        """
        light_dir:np.ndarray = utils.normalize(self.position - hit.point)

        shadow_origin:np.ndarray = hit.point + utils.HIT_TOLERANCE * hit.normal

        shadow_ray:Ray = Ray(shadow_origin, light_dir)

        shadow_intersection: Hit | Light | None = world.get_nearest_hit(shadow_ray)
        
        # Verificação adicional
        if shadow_intersection is self:
            r:float = utils.distance(hit.point, self.position)
            light_intensity:float = self.power / pow(r, 2)

            return light_intensity, light_dir
        else:
            return 0.0, np.array([0.0, 0.0, 0.0])


    def intersects(self, ray:Ray) -> 'Light | None':
        """
        Checks if given ray intersects with this light

        Returns the self light object if intersection is found
        Returns None if no intersection is detected
        """
        to_light = self.position - ray.origin
        t = np.dot(to_light, ray.direction)

        if t < 0:
            return None
        
        estimated_hit = ray.at(t)

        if np.allclose(estimated_hit, self.position, atol=utils.HIT_TOLERANCE):
            return self
        else:
            return None
