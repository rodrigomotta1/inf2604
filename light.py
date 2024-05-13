import numpy as np
import utils
import color as colors

from ray import Ray

class Light:
    def __init__(self, position:np.ndarray, power:float, shape=None, color:np.ndarray = colors.WHITE) -> None:
        self.position = position
        self.power = power
        self.shape = shape # NOTE: If shape is none, then light is a point light
        self.color = color
    
    def radiance(self, world, hit):
        light_dir = utils.normalize(self.position - hit.point)
        shadow_ray = Ray(hit.point, light_dir)

        shadow_hit = world.get_nearest_light_hit(shadow_ray, self)

        if shadow_hit:
            r = utils.distance(hit.point, self.position)
            light_intensity = self.power / pow(r, 2)

            return (light_intensity,light_dir)
        else:
            return (colors.BLACK, colors.BLACK)