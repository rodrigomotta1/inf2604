import numpy as np
import utils

class Ray:
    def __init__(self, origin:np.ndarray, direction:np.ndarray) -> None:
        self.origin = origin
        self.direction = utils.normalize(direction)
    
    def __repr__(self) -> str:
        return f"[Ray] origin={self.origin} direction={self.direction}"
    
    def at(self, t:float) -> np.ndarray:
        """
        Estimates point at given t
        Shortly, implements the ray equation r(t) = o + t*d
        """
        return self.origin + t * self.direction
    
    def transform(self, matrix: np.ndarray) -> 'Ray':
        """
        Applies transformation to self ray origin and direction based on given matrix.
        Returns a new Ray with transformed parameters
        """
        homogenous_origin:np.ndarray = np.concatenate((self.origin, [1.0]))
        homogenous_direction:np.ndarray = np.concatenate((self.direction, [0.0]))

        transformed_origin = matrix @ homogenous_origin
        transformed_direction = matrix @ homogenous_direction

        return Ray(transformed_origin[:3], utils.normalize(transformed_direction[:3]))