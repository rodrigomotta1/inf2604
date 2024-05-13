import numpy as np


class Hit:
    def __init__(self, 
        point:np.ndarray,
        normal:np.ndarray,
        backface:bool
        # NOTE: Maybe receive hittable instance and root t here also
    ) -> None:
        self.point = point
        self.normal = normal
        self.backface = backface

    def distance_to_origin(self, camera_center:np.ndarray = np.array([0.0, 0.0, 1.0])) -> float:
        # NOTE: maybe camera_center wasnt supposed to be passed here..
        return float(np.linalg.norm(self.point - camera_center))