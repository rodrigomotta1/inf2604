import utils
import color as colors
import numpy as np

from hit import Hit
from PIL import Image
from ray import Ray
from tqdm import tqdm
from world import World
from light import Light


class Camera:
    def __init__(
            self, 
            world:World,
            look_at:np.ndarray = np.array([0.0, 0.0, 0.0]),
            up:np.ndarray = np.array([0.0, 1.0, 0.0]),
            aspect_ratio:float = 4.0 / 3.0,
            width:int = 400,
            center:np.ndarray = np.array([0.0, 0.0, 1.0]),
            focal_lenght:float = 1.0,
            samples_per_pixel:int = 1,

        ) -> None:
        # Default data
        self.world = world
        self.width = width
        self.aspect_ratio = aspect_ratio
        self.center = center
        self.focal_length = focal_lenght
        self.look_at = look_at
        self.up = up

        # Sampling rate
        self.samples_per_pixel = samples_per_pixel
        self._pixel_samples_scale = 1.0 / self.samples_per_pixel

        # Define viewport dimensions
        self.height:int = int(self.width / self.aspect_ratio)
        self.viewport_height:float = 2.0
        self.viewport_width:float = self.viewport_height * (float(self.width) / self.height)

        # Create pixel matrix
        self.pixels = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        # Calculate the orthonormal basis vectors for the camera orientation
        self.z_axis = utils.normalize(self.center - self.look_at)
        self.x_axis = utils.normalize(np.cross(self.up, self.z_axis))
        self.y_axis = np.cross(self.x_axis, self.z_axis)

        # Calculate vector across the horizontal and down the vertical viewport edges
        self.viewport_u:np.ndarray = self.viewport_width * self.x_axis
        self.viewport_v:np.ndarray = self.viewport_height * self.y_axis

        # Calculate the horizontal and vertical delta vectors from pixel to pixel
        self.pixel_delta_u:np.ndarray = self.viewport_u / self.width
        self.pixel_delta_v:np.ndarray = self.viewport_v / self.height

        # Calculate location of upper left pixel
        self.viewport_upper_left:np.ndarray = self.center - (self.focal_length * self.z_axis) - self.viewport_u/2 - self.viewport_v/2

        self.pixel_00_location:np.ndarray = self.viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)


    def render(self, output_filepath:str = "output.png") -> None:
        """
        Cast rays and evaluates each color through auxiliary utility function
        """
        _t_iter:int = self.height * self.width * self.samples_per_pixel
        _progress_bar = tqdm(total=_t_iter, desc="Progress", unit="iter")

        for j in range(0, self.height):
            for i in range(0, self.width):
                pixel_color:np.ndarray = colors.BLACK

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
        """
        Trigger color evaluation if ray hits anything (light source or hittable object)
        If no intersection is found, then return black as color
        """
        intersection:Hit | Light | None = self.world.get_nearest_hit(ray)

        if isinstance(intersection, Hit):
            return intersection.instance.material.eval(self.world, intersection, ray)
        
        elif isinstance(intersection, Light):
            return intersection.color
        
        else:
            return colors.BLACK


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

        return Ray(self.center, utils.normalize(pixel_sample - self.center))

    