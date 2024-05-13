import numpy as np
import utils
import color as colors

class Light:
    def __init__(self, position:np.ndarray, power:float, shape=None, color:np.ndarray = colors.WHITE) -> None:
        self.position = position
        self.power = power
        self.shape = shape # NOTE: If shape is none, then light is a point light
        self.color = color
    
    def radiance(self, hit):
        light_dir = utils.normalize(self.position - hit.point)
        r = utils.distance(hit.point, self.position)
        light_intensity = self.power / pow(r, 2)

        return (light_intensity,light_dir)