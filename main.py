import numpy as np


from sphere import Sphere
from world import World
from hittable import Hittable
from plane import Plane
from camera import Camera

# def ray_color(ray:Ray, world:World) -> np.ndarray:
#     hit:Hit | None = world.get_nearest_hit(ray)

#     if hit:
#         # print(f"a")
#         # n = normalize(ray.at(hit) - np.array([0.0, 0.0, -1.0]))
#         return 0.5 * np.array([
#             hit.normal[0] + 1,
#             hit.normal[1] + 1,
#             hit.normal[2] + 1,
#         ])
#         # return 0.5 * (hit.normal + np.array([1.0, 1.0, 1.0]))
#     else:
#         # print(f"b")
#         return np.array([0.0, 0.0, 0.0])

def main():
    # Image
    # aspect_ratio:float = 4.0 / 3.0
    # image_width:int = 400
    # image_height:int = max(1, int(image_width / aspect_ratio))

    # # Camera
    # focal_length:float = 1.0
    # viewport_height:float = 2.0
    # viewport_width:float = viewport_height * (float(image_width) / image_height)
    # camera_center:np.ndarray = np.array([0.0, 0.0, 0.0])
    
    # viewport_u:np.ndarray = np.array([viewport_width, 0.0, 0.0])
    # viewport_v:np.ndarray = np.array([0, -viewport_height, 0.0])

    # pixel_delta_u:np.ndarray = viewport_u / image_width
    # pixel_delta_v:np.ndarray = viewport_v / image_height

    # viewport_upper_left:np.ndarray = camera_center - np.array([0.0, 0.0, focal_length]) - (viewport_u / 2) - (viewport_v / 2)

    # pixel_00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v) # TODO: This 0.5 need to be changed in order to make sampling

    
    # World
    world = World([
        Hittable(surface=Sphere(np.array([0.0, 0.0, -1.0]), 0.5)),
        Hittable(surface=Sphere(np.array([2.0, 0.0, -3.0]), 0.5)),
        Hittable(surface=Plane(np.array([0.0, 3.0, 0.0]), np.array([0.0, 1.0, 0.0])))
    ])

    # Cam
    camera = Camera(world=world)

    camera.render()
    
    # print(f"\nDone")
    # image.show()


if __name__ == "__main__":
    main()