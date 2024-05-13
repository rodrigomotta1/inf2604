import numpy as np
import utils
import color as colors

class Material():
    def __init__(self, color:np.ndarray, diffuse:float, specular:float, shininess:float, ambient:float = 0.05,  debug:bool = False) -> None:
        self.diffuse = diffuse
        self.specular = specular
        self.ambient = ambient
        self.shininess = shininess
        self.color = color
        self.debug = debug
    
    def eval(self, world, hit, ray):
        """
        Evaluate material color considering traced ray, world lights and hit informations.
        """
        if self.debug:
            # Returns color based on hit normals
            return 0.5 * np.array([
                hit.normal[0] + 1,
                hit.normal[1] + 1,
                hit.normal[2] + 1,
            ])
        else:
            # Phong illumination model implementation
            color:np.ndarray = colors.BLACK
            viewer_direction:np.ndarray = utils.normalize(ray.origin - hit.point)

            # Ambient
            color = color + (self.color * self.ambient)

            for light in world.lights:
                light_intensity, light_dir = light.radiance(hit)

                # Diffuse
                color = color + (self.color * self.diffuse * light_intensity * max(0, np.dot(hit.normal, light_dir)))

            
            # implementation logic..

            return color