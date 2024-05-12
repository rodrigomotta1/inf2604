import numpy as np

from sphere import Sphere
from world import World
from hittable import Hittable
from plane import Plane
from camera import Camera


def main():
    world = World([
        Hittable(surface=Sphere(np.array([0.0, 0.0, -1.0]), 0.5)),
        Hittable(surface=Sphere(np.array([2.0, 2.0, -3.0]), 0.5)),
        Hittable(surface=Plane(np.array([0.0, 3.0, 0.0]), np.array([0.0, 1.0, 0.0])))
    ])

    # Cam
    camera = Camera(world=world)

    camera.render()


if __name__ == "__main__":
    main()