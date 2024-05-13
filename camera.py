import utils
import numpy as np

from hit import Hit
from PIL import Image
from ray import Ray
from tqdm import tqdm
from world import World

# NOTE: Maybe create a function to get position of pixel based on input i, j (function receives pixel position i, j and returns its 3D position)
class Camera:
    def __init__(
            self, 
            world:World,
            aspect_ratio:float = 4.0 / 3.0,
            width:int = 400,
            center:np.ndarray = np.array([0.0, 0.0, 0.0]),
            focal_lenght:float = 1.0,
            samples_per_pixel:int = 10,

        ) -> None:
        # Default data
        self.world = world
        self.width = width
        self.aspect_ratio = aspect_ratio
        self.center = center
        self.focal_length = focal_lenght

        # Sampling rate
        self.samples_per_pixel = samples_per_pixel
        self._pixel_samples_scale = 1.0 / self.samples_per_pixel

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
        _t_iter:int = self.height * self.width * self.samples_per_pixel
        _progress_bar = tqdm(total=_t_iter, desc="Progress", unit="iter")

        for j in range(0, self.height):
            for i in range(0, self.width):
                # pixel_center:np.ndarray = self.pixel_00_location + (i * self.pixel_delta_u) + (j * self.pixel_delta_v)
                # ray = Ray(self.center, pixel_center - self.center)

                # self.pixels[j, i] = utils.write_color(self.ray_color(ray))

                # _progress_bar.update(1)
                pixel_color:np.ndarray = np.array([0.0, 0.0, 0.0]) # Initial pixel color. Will be defined as the average of samples!

                # For each predefined sample, generates a ray and calculates its color contribution, updating initial_color value
                for sample in range(0, self.samples_per_pixel):
                    ray = self.sample_ray(i, j)
                    pixel_color += self.ray_color(ray)
                    _progress_bar.update(1)
            
                avg_samples_color:np.ndarray =  np.divide(pixel_color, self.samples_per_pixel)
            
                self.pixels[j, i] = utils.write_color(avg_samples_color)


        # NOTE: Maybe put this in other function
        image = Image.fromarray(self.pixels)
        image.save(output_filepath)


    def ray_color(self, ray:Ray) -> np.ndarray:
        hit:Hit | None = self.world.get_nearest_hit(ray)

        if hit:
            # return 0.5 * np.array([
            #     hit.normal[0] + 1,
            #     hit.normal[1] + 1,
            #     hit.normal[2] + 1,
            # ])
            return hit.instance.material.eval(self.world, hit, ray)
        else:
            return np.array([0.0, 0.0, 0.0])


    def sample_ray(self, pixel_i:int, pixel_j:int) -> Ray:
        """
        Generates a random ray with origin at the camera center and direction to the surrounding of current pixel (i, j)
        The direction point is randomly chosen by a uniform distribution function
        """
        offset:np.ndarray = utils.sample_square()

        pixel_sample:np.ndarray = (
            self.pixel_00_location
            + ((pixel_i + offset[0]) * self.pixel_delta_u)
            + ((pixel_j + offset[1]) * self.pixel_delta_v)
        )

        return Ray(self.center, pixel_sample - self.center)

    