import numpy as np

class Ray:
    def __init__(self, origin:np.ndarray, direction:np.ndarray) -> None:
        self.origin = origin
        self.direction = direction
    
    def __repr__(self) -> str:
        return f"[Ray] origin={self.origin} direction={self.direction}"
    
    def at(self, t:float) -> np.ndarray:
        """
        Estimates point at given t
        Shortly, implements the ray equation r(t) = o + t*d
        """
        return self.origin + t * self.direction