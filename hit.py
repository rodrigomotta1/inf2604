import numpy as np


class Hit:
    def __init__(self, 
        position:np.ndarray,
        normal:np.ndarray,
        backface:bool,
        instance, # The hittable object associated with this hit
        t:float
        # NOTE: Maybe receive hittable instance and root t here also
    ) -> None:
        self.position = position
        self.normal = normal
        self.backface = backface
        self.instance = instance
        self.t = t

    def distance_to_origin(self, camera_center:np.ndarray = np.array([0.0, 0.0, 1.0])) -> float:
        # NOTE: maybe camera_center wasnt supposed to be passed here..
        return float(np.linalg.norm(self.position - camera_center))