import numpy as np
import color as colors

from sphere import Sphere
from world import World
from hittable import Hittable
from plane import Plane
from camera import Camera
from light import Light
from material import Material


def main():
    world = World(
        hittables=[
            Hittable(
                surface=Sphere(np.array([0.0, 0.0, -1.0]), 0.5),
                material=Material(colors.RED, 0.2, 0.5, 2.0, debug=True)
            ),
            Hittable(
                surface=Sphere(np.array([2.0, 2.0, -3.0]), 0.5),
                material=Material(colors.GREEN, 0.2, 0.5, 2.0, debug=True)
            ),
            Hittable(
                surface=Plane(np.array([0.0, 3.0, 0.0]), np.array([0.0, 1.0, 0.0])),
                material=Material(colors.WHITE / 2, 0.2, 0.5, 2.0, debug=True)
            )
        ],
        lights=[
            Light(np.array([0.0, 3.0, -1.0]), 2.0)
        ]
    )

    # Cam
    camera = Camera(world=world)

    camera.render()


if __name__ == "__main__":
    main()