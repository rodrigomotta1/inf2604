import numpy as np

class Light:
    def __init__(self, position:np.ndarray, power:float, shape=None) -> None:
        self.position = position
        self.power = power
        self.shape = shape # NOTE: If shape is none, then light is a point light
    