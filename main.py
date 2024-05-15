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
                surface=Sphere(np.array([0.0, 0.0, -2.5]), 0.5),
                material=Material(colors.YELLOW, 0.2, 0.5, 50.0, debug=False)
            ),
            Hittable(
                surface=Sphere(np.array([1.5, 0.0, -2.0]), 0.5),
                material=Material(colors.DARK_GREEN, 0.1, 0.5, 50.0, debug=False)
            ),
            Hittable(
                surface=Sphere(np.array([-1.5, 0.0, -2.0]), 0.5),
                material=Material(colors.RED, 0.1, 0.5, 50.0, debug=False)
            ),
            # Hittable(
            #     surface=Sphere(np.array([0.0, -200.5, -2.0]), 200),
            #     material=Material(np.array([0.7, 0.7, 0.7]), 0.1, 0.5, 2.0, debug=False)
            # )
            Hittable(
                surface=Plane(np.array([0.0, 0.5, 0.0]), np.array([0.0, 1.0, 0.0])),
                material=Material(np.array([0.7, 0.7, 0.7]), 0.2, 0.5, 2.0, debug=False)
            )
        ],
        lights=[
            Light(np.array([0.0, 2.0, -2.0]), 10.0)
        ]
    )

    # Cam
    camera = Camera(world=world)

    camera.render()


if __name__ == "__main__":
    main()