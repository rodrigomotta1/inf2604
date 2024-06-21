
class Hittable:
    def __init__(self, surface, material) -> None:
        self.material = material
        self.surface = surface

    def intersects(self, ray):
        return self.surface.intersects(self, ray)
    
    # def eval(self, )