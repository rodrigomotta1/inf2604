import numpy as np


class Hit:
    def __init__(self, 
        position:np.ndarray,
        normal:np.ndarray,
        backface:bool,
        instance, # The hittable object associated with this hit
        t:float
    ) -> None:
        self.position = position
        self.normal = normal
        self.backface = backface
        self.instance = instance
        self.t = t