import numpy as np
import utils
import color as colors

from ray import Ray
from hit import Hit

class Light:
    def __init__(self, position:np.ndarray, power:float, shape=None, color:np.ndarray = colors.WHITE) -> None:
        self.position = position
        self.power = power
        self.shape = shape # NOTE: If shape is none, then light is a point light
        self.color = color
    
    def radiance(self, world, hit):
        light_dir = utils.normalize(self.position - hit.point)
        shadow_ray = Ray(hit.point, light_dir)

        # r = utils.distance(hit.point, self.position)
        # light_intensity = self.power / pow(r, 2)

        # return (light_intensity,light_dir)

        # Check intersections
        # shadow_hit = None

        for hittable in world.hittables:
            shadow_hit = hittable.intersects(shadow_ray)
            # if isinstance(hit_evaluation, Light):
            #     print(f"Light!")

            if shadow_hit is not None:
                return (colors.BLACK, colors.BLACK)
        
        r = utils.distance(hit.point, self.position)
        light_intensity = self.power / pow(r, 2)

        return (light_intensity,light_dir)
        
    def distance_to_origin(self, camera_center:np.ndarray = np.array([0.0, 0.0, 0.0])):
        return utils.distance(camera_center, self.position)
    
    def intersects(self, ray:Ray) -> 'Light | None':
        # Calcula o vetor do ponto de origem até o ponto dado
        vetor_ponto = self.position - ray.origin
        
        # Calcula o parâmetro 't' usando a projeção do vetor do ponto na direção do raio
        t = np.dot(vetor_ponto, ray.origin)
        
        # Verifica se o ponto está na direção do raio
        if t >= 0:
            # Calcula a posição no raio correspondente a 't'
            ponto_no_raio = ray.origin + t * ray.direction
            
            # Calcula a distância entre o ponto dado e o ponto no raio
            distancia = np.linalg.norm(self.position - ponto_no_raio)
            
            # Se a distância for muito próxima de zero, consideramos que o ponto está no raio
            if np.isclose(distancia, utils.HIT_TOLERANCE):
                return self
        
        return None
