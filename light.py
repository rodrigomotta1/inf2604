import numpy as np
import utils

class Light:
    def __init__(self, position:np.ndarray, power:float, shape=None) -> None:
        self.position = position
        self.power = power
        self.shape = shape # NOTE: If shape is none, then light is a point light
    
    def radiance(self, hit):
        light_dir = utils.normalize(self.position - hit.point)
        r = utils.distance(hit.point, self.position)
        light_intensity = self.power / pow(r, 2)

        return (light_intensity,light_dir)