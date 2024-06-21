import numpy as np


class Hit:
    """
    Abstraction of a intersection object.
    Only holds important information about hit between ray and object (light source or hittable surface)
    """
    def __init__(self, 
        point:np.ndarray,
        normal:np.ndarray,
        backface:bool,
        instance, # The hittable object associated with this hit
        t:float
    ) -> None:
        self.point = point
        self.normal = normal
        self.backface = backface
        self.instance = instance
        self.t = t