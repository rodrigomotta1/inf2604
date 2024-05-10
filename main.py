import numpy as np
import math

from tqdm import tqdm
from PIL import Image
from utils import write_color, normalize
from ray import Ray
from sphere import Sphere
from world import World
from hit import Hit
from hittable import Hittable
from plane import Plane

def ray_color(ray:Ray, world:World) -> np.ndarray:
    hit:Hit | None = world.get_nearest_hit(ray)

    if hit:
        # print(f"a")
        # n = normalize(ray.at(hit) - np.array([0.0, 0.0, -1.0]))
        return 0.5 * np.array([
            hit.normal[0] + 1,
            hit.normal[1] + 1,
            hit.normal[2] + 1,
        ])
        # return 0.5 * (hit.normal + np.array([1.0, 1.0, 1.0]))
    else:
        # print(f"b")
        return np.array([0.0, 0.0, 0.0])

def main():
    # Image
    aspect_ratio:float = 4.0 / 3.0
    image_width:int = 400
    image_height:int = max(1, int(image_width / aspect_ratio))

    # Camera
    focal_length:float = 1.0
    viewport_height:float = 2.0
    viewport_width:float = viewport_height * (float(image_width) / image_height)
    camera_center:np.ndarray = np.array([0.0, 0.0, 0.0])
    
    viewport_u:np.ndarray = np.array([viewport_width, 0.0, 0.0])
    viewport_v:np.ndarray = np.array([0, -viewport_height, 0.0])

    pixel_delta_u:np.ndarray = viewport_u / image_width
    pixel_delta_v:np.ndarray = viewport_v / image_height

    viewport_upper_left:np.ndarray = camera_center - np.array([0.0, 0.0, focal_length]) - (viewport_u / 2) - (viewport_v / 2)

    pixel_00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v) # TODO: This 0.5 need to be changed in order to make sampling
    
    # World
    world = World([
        Hittable(surface=Sphere(np.array([0.0, 0.0, -1.0]), 0.5)),
        Hittable(surface=Sphere(np.array([2.0, 0.0, -3.0]), 0.5)),
        Hittable(surface=Plane(np.array([0.0, 3.0, 0.0]), np.array([0.0, 1.0, 0.0])))
    ])

    # Render
    pixels = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    # Progress
    _t_iter:int = image_height * image_width
    _progress_bar = tqdm(total=_t_iter, desc="Progress", unit="iter")

    for j in range(0, image_height):
        for i in range(0, image_width):
            pixel_center:np.ndarray = pixel_00_loc + (i * pixel_delta_u) + (j * pixel_delta_v)
            ray = Ray(camera_center, pixel_center - camera_center)

            pixels[j, i] = write_color(ray_color(ray, world))

            _progress_bar.update(1)

    image = Image.fromarray(pixels)
    image.save("output.png")
    # print(f"\nDone")
    # image.show()


if __name__ == "__main__":
    main()