import math
import numpy as np
import random

HIT_TOLERANCE = 1e-6

X_AXIS = np.array([1.0, 0.0, 0.0])
Y_AXIS = np.array([0.0, 1.0, 0.0])
Z_AXIS = np.array([0.0, 0.0, 1.0])


def degrees_to_radians(degrees:float) -> float:
    return degrees * math.pi / 180.0

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
    norm:float = float(np.linalg.norm(vector))

    # If nomr is almost 0, then its not possible to normalize the vector, so return itself 
    if norm < HIT_TOLERANCE:
        return vector
    else:
        return vector / np.linalg.norm(vector)


def sample_square() -> np.ndarray:
    """
    Generates a random sample point within the unit square centered at the origin. We then transform the random sample from this ideal square back to the particular pixel we're currently sampling
    
    In other words, generates a real number to offset the ray direction from pixel center randomly
    """
    return np.array([
        random.uniform(0, 1) - 0.5,
        random.uniform(0, 1) - 0.5,
        0.0
    ])

def distance(point_a:np.ndarray, point_b:np.ndarray) -> float:
    """
    Returns distnace between point_a and point_b.
    In other words, the magnitude of the vector point_a - point_b.
    """
    return float(np.linalg.norm(point_a - point_b))

def reflect(vector:np.ndarray, ref:np.ndarray) -> np.ndarray:
    """
    Returns a vector reflected along given ref
    """
    # return ((2 * np.dot(ref, vector)) * ref) - vector
    return vector - 2 * np.dot(vector, ref) * ref

def refract(v: np.ndarray, n: np.ndarray, ior: float) -> np.ndarray:
    cosi = max(-1, min(1, np.dot(v, n)))
    etai = 1
    etat = ior
    if cosi < 0:
        cosi = -cosi
    else:
        etai, etat = etat, etai
        n = -n
    eta = etai / etat
    k = 1 - eta ** 2 * (1 - cosi ** 2)
    if k < 0:
        return np.zeros(3)
    else:
        return eta * v + (eta * cosi - np.sqrt(k)) * n

    
def normal_to_global(normal:np.ndarray):
    """
    Converte uma direção normal ao plano de um hemisfério para uma direção global.
    
    Parâmetros:
    - normal: Um vetor normal ao plano do hemisfério, normalizado para ter comprimento unitário.
    
    Retorna:
    - Uma direção global aleatória no hemisfério, também normalizada.
    """
    # Gera um ângulo de elevação aleatório entre 0 e π
    theta = np.arccos(np.random.uniform(-1, 1))
    
    # Gera um ângulo azimutal aleatório entre 0 e 2π
    phi = 2 * np.pi * np.random.uniform(0, 1)
    
    # Calcula os componentes x, y, z da direção global
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    
    # Normaliza a direção global para ter comprimento unitário
    global_direction = np.array([x, y, z]) / np.linalg.norm(np.array([x, y, z]))
    
    return global_direction

