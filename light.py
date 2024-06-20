import numpy as np
import utils
import color as colors

from ray import Ray
from hit import Hit
from typing import Tuple
# from world import World

class Light:
    def __init__(self, position:np.ndarray, power:float, shape=None, color:np.ndarray = colors.WHITE) -> None:
        self.position = position
        self.power = power
        self.shape = shape # NOTE: If shape is none, then light is a point light
        self.color = color
    
    def radiance(self, world, hit:Hit) -> Tuple[float, np.ndarray]:
        light_dir:np.ndarray = self.position - hit.point
        # light_dir:np.ndarray = utils.normalize(self.position - hit.point)
        _light_dist:float = float(np.linalg.norm(self.position - hit.point))

        shadow_ray:Ray = Ray(hit.point, light_dir)

        shadow_intersection: Hit | Light | None = world.get_nearest_hit(shadow_ray)

        # if shadow_intersection == self or shadow_intersection is None:
        #     r:float = utils.distance(hit.point, self.position)
        #     light_intensity:float = self.power / pow(r, 2)

        #     return (light_intensity, utils.normalize(light_dir))
        # else:
        #     return (0.0, colors.BLACK)

        r:float = utils.distance(hit.point, self.position)
        light_intensity:float = self.power / pow(r, 2)

        return (light_intensity, utils.normalize(light_dir))

        # r = utils.distance(hit.point, self.position)
        # light_intensity = self.power / pow(r, 2)

        # return (light_intensity,light_dir)

        # Check intersections
        # shadow_hit = None

        # for hittable in world.hittables:
        #     shadow_hit:Hit = hittable.intersects(shadow_ray)
            # if isinstance(hit_evaluation, Light):
            #     print(f"Light!")


            # if shadow_hit is not None:
            #     if shadow_hit.t < _light_dist:
            #         return (colors.BLACK, colors.BLACK)
        

        # return (light_intensity, light_dir)
    
    def intersects(self, ray:Ray) -> 'Light | None':
        """
        Checks if given ray intersects with this light

        Returns the self light object if intersection is found
        Returns None if no intersection is detected
        """
        to_light = self.position - ray.origin
        t = np.dot(to_light, ray.direction)

        # if t < 0:
        #     return None
        
        estimated_hit = ray.at(t)

        if np.allclose(estimated_hit, self.position, atol=utils.HIT_TOLERANCE):
            return self
        else:
            return None

        # if pos_at_ray == self.position:
        #     return True
