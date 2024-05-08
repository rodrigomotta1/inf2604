import numpy as np

def write_color(pixel_color: np.ndarray) -> np.ndarray:
    """
    Maps float color percentages to int rgb value triplets
    """
    return np.array([
        min(255, max(0, int(255 * pixel_color[0]))),
        min(255, max(0, int(255 * pixel_color[1]))),
        min(255, max(0, int(255 * pixel_color[2]))),
    ])

def normalize(vector:np.ndarray) -> np.ndarray:
    """
    Receives a arbitrary vector and returns its normalized version
    """
    return vector / np.linalg.norm(vector)