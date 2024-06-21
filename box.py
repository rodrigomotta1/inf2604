import numpy as np
import utils

from ray import Ray
from hit import Hit
from utils import HIT_TOLERANCE, normalize

class Box:
    def __init__(self, min_corner: np.ndarray, max_corner: np.ndarray, ) -> None:
        self.min_corner = min_corner
        self.max_corner = max_corner

    def intersects(self, hittable: object, ray: Ray) -> Hit | None:
        t0:np.ndarray = (self.min_corner - ray.origin) / ray.direction
        t1:np.ndarray = (self.max_corner - ray.origin) / ray.direction

        t_near:np.ndarray = np.minimum(t0, t1)
        t_far:np.ndarray = np.maximum(t0, t1) 

        t_min:float = np.max(t_near)
        t_max:float = np.min(t_far)

        if t_min > t_max or t_max < 0:
            return None
        
        t_hit:float = t_min if t_min > 0 else t_max
        hit_point:np.ndarray = ray.at(t_hit)

        normal_at_hit:np.ndarray = self._calculate_normal(hit_point)
        is_backface:bool = np.dot(ray.direction, normal_at_hit) > 0
        normal_at_hit = -normal_at_hit if is_backface else normal_at_hit

        return Hit(hit_point, normal_at_hit, is_backface, instance=hittable, t=t_hit)

    def _calculate_normal(self, point:np.ndarray) -> np.ndarray:
        """
        Auxiliary method to evaluate normal at given box point
        """
        center = (self.min_corner + self.max_corner) * 0.5
        extent = (self.max_corner - self.min_corner) * 0.5

        local_hit_point = (point - center) / extent

        if abs(local_hit_point[0]) > 1 - utils.HIT_TOLERANCE:
            return np.array([np.sign(local_hit_point[0]), 0, 0])
        
        elif abs(local_hit_point[1]) > 1 - utils.HIT_TOLERANCE:
            return np.array([0, np.sign(local_hit_point[1]), 0])
        
        elif abs(local_hit_point[2]) > 1 - utils.HIT_TOLERANCE:
            return np.array([0, 0, np.sign(local_hit_point[2])])
        
        else:
            return np.array([0, 0, 0])
    
    def rotate(self, axis: np.ndarray, angle: float):
        rotation_matrix = self._get_rotation_matrix(axis, angle)
        new_min_corner, new_max_corner = self._apply_transformation(rotation_matrix)
        self.min_corner = new_min_corner
        self.max_corner = new_max_corner

        exit()

        return self
    
    def translate(self, translation: np.ndarray):
        translation_matrix = self._get_translation_matrix(translation)
        self._apply_transformation(translation_matrix)

        return self

    def shear(self, shear_factors: np.ndarray):
        shear_matrix = self._get_shear_matrix(shear_factors)
        self._apply_transformation(shear_matrix)

        return self
    
    def _get_rotation_matrix(self, axis: np.ndarray, angle: float) -> np.ndarray:
        axis = utils.normalize(axis)
        cos_theta = np.cos(angle)
        sin_theta = np.sin(angle)
        one_minus_cos = 1.0 - cos_theta

        x, y, z = axis
        return np.array([
            [cos_theta + x*x*one_minus_cos, x*y*one_minus_cos - z*sin_theta, x*z*one_minus_cos + y*sin_theta],
            [y*x*one_minus_cos + z*sin_theta, cos_theta + y*y*one_minus_cos, y*z*one_minus_cos - x*sin_theta],
            [z*x*one_minus_cos - y*sin_theta, z*y*one_minus_cos + x*sin_theta, cos_theta + z*z*one_minus_cos]
        ])

    def _get_translation_matrix(self, translation: np.ndarray) -> np.ndarray:
        matrix = np.eye(4)
        matrix[:3, 3] = translation
        return matrix

    def _get_shear_matrix(self, shear_factors: np.ndarray) -> np.ndarray:
        shear_matrix = np.eye(4)
        shear_matrix[0, 1] = shear_factors[0]
        shear_matrix[0, 2] = shear_factors[1]
        shear_matrix[1, 0] = shear_factors[2]
        shear_matrix[1, 2] = shear_factors[3]
        shear_matrix[2, 0] = shear_factors[4]
        shear_matrix[2, 1] = shear_factors[5]
        return shear_matrix

    def _apply_transformation(self, transformation_matrix: np.ndarray):
        print(f"{self.min_corner} | {self.min_corner.shape}")
        # Adiciona a dimensão homogênea aos vértices da caixa
        min_corner_homogeneous = np.append(self.min_corner, 1)
        max_corner_homogeneous = np.append(self.max_corner, 1)

        # Converte os vértices para um formato adequado para multiplicação
        min_corner_homogeneous = min_corner_homogeneous.reshape(1, 4)
        max_corner_homogeneous = max_corner_homogeneous.reshape(1, 4)

        # Aplica a transformação aos vértices da caixa
        transformed_min_corner = np.dot(min_corner_homogeneous, transformation_matrix.T)[:3]
        transformed_max_corner = np.dot(max_corner_homogeneous, transformation_matrix.T)[:3]

        # Cria cópias dos cantos transformados
        new_min_corner = np.minimum(transformed_min_corner, transformed_max_corner)
        new_max_corner = np.maximum(transformed_min_corner, transformed_max_corner)

        # Retorna os novos cantos sem modificar os atributos do objeto
        return new_min_corner.flatten(), new_max_corner.flatten()



    