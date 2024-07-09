import numpy as np
import color as colors
import utils

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
gray_glossy = Material(colors.WHITE, 0.1, 0.001, 70.0, debug=False)
blue_metal = Material(colors.BLUE, 0.1, 0.001, 70, reflection=0.5)
gray_metal = Material(colors.WHITE, 0.1, 0.001, 70, reflection=0.5)
green_metal = Material(colors.GREEN, 0.1, 0.001, 70, reflection=0.5)
red_metal = Material(colors.RED, 0.1, 0.001, 70, reflection=0.5)
gray_transparent = Material(colors.WHITE, 0.1, 0.001, 70, reflection=0.0, refraction=0.7, ior=1.5)


small_box_surface = surface=Box(
    np.array([0.0, 0.0, 0.0]), 
    np.array([1.65, 1.65, 1.65])
).translate(np.array([3.8, 0.0, 1.5])).rotate(-18, utils.Y_AXIS)


big_box_surface = surface=Box(
    np.array([0.0, 0.0, 0.0]),
    np.array([1.65, 3.3, 1.65])
).translate(np.array([0.15, 0.0, 1.5])).rotate(22.5, utils.Y_AXIS)


balls = World(
        hittables=[
            Hittable(
                surface=Sphere(np.array([-1.1, 0.0, -1.5]), 0.5),
                material=red_glossy
            ),
            Hittable(
                surface=Sphere(np.array([0.0, 0.0, -1.5]), 0.5),
                material=green_glossy
            ),
            Hittable(
                surface=Sphere(np.array([1.1, 0.0, -1.5]), 0.5),
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
            # Light(np.array([0.0, 2.0, -1.5]), 38.0),
            # Light(np.array([6.0, 2.0, -1.5]), 48.0),
            Light(np.array([0.0, 2.0, -1.5]), 3.8),
            Light(np.array([6.0, 2.0, -1.5]), 4.8),
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
            material=gray_metal
        ),
        # Big box
        Hittable(
            surface=big_box_surface,
            material=gray_metal
        ),
    ],
    lights=[
        Light(np.array([2.775, 5.46, 2.775]), 3.0),
        # Light(np.array([1.65, 1.65, 0.3]), 38.0),
    ]
)