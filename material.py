import numpy as np

class Material():
    def __init__(self, color:np.ndarray, diffuse:float, specular:float, shininess:float, debug:bool = False) -> None:
        self.diffuse = diffuse
        self.specular = specular
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
            color:np.ndarray = self.color
            
            # implementation logic..

            return color