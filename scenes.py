import numpy as np
import color as colors

from world import World
from sphere import Sphere
from material import Material
from plane import Plane
from hittable import Hittable
from light import Light
from box import Box

red_glossy = Material(colors.RED, 0.1, 0.5, 70.0, debug=False)
green_glossy = Material(colors.GREEN, 0.1, 0.5, 70.0, debug=False)
blue_glossy = Material(colors.BLUE, 0.1, 0.5, 70.0, debug=False)
gray_glossy = Material(np.array([0.7, 0.7, 0.7]), 0.1, 0.5, 70.0, debug=False)

# small_box_surface = surface=Box(
#                 np.array([-0.1, -0.1, 0.0]), 
#                 np.array([5.65, 0, 5.55])
#             ).translate(np.array([3.4, 1.2, 3.65])).rotate(np.array([0.0, 1.0, 0.0]), -18.0)


small_box_surface = surface=Box(
                np.array([-0.1, -0.1, 0.0]), 
                np.array([5.65, 0, 5.55])
            )


balls = World(
        hittables=[
            Hittable(
                surface=Sphere(np.array([-1.5, 0.0, -1.5]), 0.5),
                material=red_glossy
            ),
            Hittable(
                surface=Sphere(np.array([0.0, 0.0, -1.5]), 0.5),
                material=green_glossy
            ),
            Hittable(
                surface=Sphere(np.array([1.5, 0.0, -1.5]), 0.5),
                material=blue_glossy
            ),
            Hittable(
                surface=Plane(np.array([0.0, -0.5, 0.0]), np.array([0.0, 1.0, 0.0])),
                material=gray_glossy
            ),
            Hittable(
                surface=Plane(np.array([0.0, -0.5, -4.0]), np.array([0.0, 0.0, 1.0])),
                material=gray_glossy
            ),
        ],
        lights=[
            Light(np.array([0.0, 2.0, -1.5]), 38.0),
            Light(np.array([6.0, 2.0, -1.5]), 48.0),
        ]
    )

cornell_box = World(
    hittables=[
        # Front
        Hittable(
            surface=Box(np.array([-0.1, -0.1, -0.1]), np.array([5.65, 5.65, 0.0])),
            material=gray_glossy
        ),
        # Left
        Hittable(
            surface=Box(np.array([-0.1, -0.1, 0.0]), np.array([0.0, 5.55, 5.55])),
            material=green_glossy
        ),
        # Right
        Hittable(
            surface=Box(np.array([5.55, -0.1, 0.0]), np.array([5.65, 5.55, 5.55])),
            material=red_glossy
        ),
        # Ceiling
        Hittable(
            surface=Box(np.array([0.0, 5.55, 0.0]), np.array([5.55, 5.65, 5.55])),
            material=gray_glossy
        ),
        # Floor
        Hittable(
            surface=Box(np.array([-0.1, -0.1, 0.0]), np.array([5.65, 0, 5.55])),
            material=gray_glossy
        ),
        # Small box
        Hittable(
            surface=small_box_surface,
            material=gray_glossy
        ),
    ],
    lights=[
        Light(np.array([2.775, 5.45, 2.775]), 38.0),
        # Light(np.array([1.65, 1.65, 0.3]), 38.0),
    ]
)