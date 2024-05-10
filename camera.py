import numpy as np
import utils

from ray import Ray
from world import World
from hit import Hit
from tqdm import tqdm
from PIL import Image


class Camera:
    def __init__(
            self, 
            world:World,
            aspect_ratio:float = 4.0 / 3.0,
            width:int = 400,
            center:np.ndarray = np.array([0.0, 0.0, 0.0]),
            focal_lenght:float = 1.0,

        ) -> None:
        # Default data
        self.world = world
        self.width = width
        self.aspect_ratio = aspect_ratio
        self.center = center
        self.focal_length = focal_lenght

        # Determine viewport dimensions
        self.height:int = int(self.width / self.aspect_ratio)
        self.viewport_height:float = 2.0
        self.viewport_width:float = self.viewport_height * (float(self.width) / self.height)

        # Create pixel matrix
        self.pixels = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        # Calculate vector across the horizontal and down the vertical viewport edges
        self.viewport_u:np.ndarray = np.array([self.viewport_width, 0.0, 0.0])
        self.viewport_v:np.ndarray = np.array([0.0, -self.viewport_height, 0.0])

        # Calculate the horizontal and vertical delta vectors from pixel to pixel
        self.pixel_delta_u:np.ndarray = self.viewport_u / self.width
        self.pixel_delta_v:np.ndarray = self.viewport_v / self.height

        # Calculate location of upper left pixel
        self.viewport_upper_left:np.ndarray = self.center - np.array([0.0, 0.0, focal_lenght]) - self.viewport_u/2 - self.viewport_v/2

        self.pixel_00_location:np.ndarray = self.viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)


    def render(self, output_filepath:str = "output.png") -> None:
        """
        Cast rays and evaluates each color through auxiliary utility function
        """
        _t_iter:int = self.height * self.width
        _progress_bar = tqdm(total=_t_iter, desc="Progress", unit="iter")

        for j in range(0, self.height):
            for i in range(0, self.width):
                pixel_center:np.ndarray = self.pixel_00_location + (i * self.pixel_delta_u) + (j * self.pixel_delta_v)
                ray = Ray(self.center, pixel_center - self.center)

                self.pixels[j, i] = utils.write_color(self.ray_color(ray))

                _progress_bar.update(1)

        # NOTE: Maybe put this in other function
        image = Image.fromarray(self.pixels)
        image.save(output_filepath)


    def ray_color(self, ray:Ray) -> np.ndarray:
        hit:Hit | None = self.world.get_nearest_hit(ray)

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

    