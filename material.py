import numpy as np
import utils
import color as colors

from world import World
from ray import Ray

class Material():
    def __init__(
            self, 
            color:np.ndarray, 
            diffuse:float, 
            specular:float, 
            shininess:float,
            reflection:float = 0.0,
            refraction:float = 0.0,
            ior:float = 1.0,
            ambient:float = 0.2, 
            debug:bool = False
        ) -> None:
        self.color = color
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflection = reflection
        self.refraction = refraction
        self.ior = ior
        self.ambient = ambient
        self.debug = debug
    
    def eval(self, world:World, hit, ray, depth:int, camera):
        """
        Evaluate material color considering traced ray, world lights and hit informations.
        Depth paramter is used to evaluate reflection and refraction of light through material
        """
        if self.debug:
            # Returns color based on hit normals
            return 0.5 * np.array([
                hit.normal[0] + 1,
                hit.normal[1] + 1,
                hit.normal[2] + 1,
            ])
        else:
            # Light evaluation
            color:np.ndarray = colors.BLACK
            viewer_direction:np.ndarray = utils.normalize(ray.origin - hit.position)

            # Including ambient light
            color = color + (self.color * self.ambient)

            for light in world.lights:
                # Get light data
                light_intensity, light_dir = light.radiance(world, hit)

                # Evalaute diffuse component
                color = color + (self.color * self.diffuse * light_intensity * max(0, np.dot(hit.normal, light_dir)))

                # Evaluate specular component
                reflected_light_dir = utils.normalize(utils.reflect(light_dir, hit.normal))

                # Accumulate color contribution by this light
                color = color + (light.color * self.specular * light_intensity * pow(max(0, np.dot(reflected_light_dir, viewer_direction)), self.shininess))
            
            if depth > 0:
                if self.reflection > 0:
                    reflected_dir = utils.reflect(ray.direction, hit.normal)
                    reflected_ray = Ray(hit.position + hit.normal * utils.HIT_TOLERANCE, reflected_dir)

                    color += self.reflection * camera.ray_color(reflected_ray, depth - 1)
                
                if self.refraction > 0:
                    refracted_dir = utils.refract(ray.direction, hit.normal, self.ior)
                    refracted_ray = Ray(hit.position - hit.normal * 1e-5, refracted_dir)
                    color += self.refraction * camera.ray_color(refracted_ray, depth - 1)


            return color