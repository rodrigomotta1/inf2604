import utils
import color as colors
import numpy as np

from hit import Hit
from PIL import Image
from ray import Ray
from tqdm import tqdm
from world import World
from light import Light

from multiprocessing import Pool, cpu_count

# Função auxiliar para inicializar cada processo com o objeto self
def _init_process(camera):
    global global_camera
    global_camera = camera

# Função global para processar um único pixel
def _process_pixel(pixel_coords):
    i, j = pixel_coords
    pixel_color = np.array([0.0, 0.0, 0.0])

    for sample in range(global_camera.samples_per_pixel):
        ray = global_camera.sample_ray(i, j)
        pixel_color += global_camera.ray_color(ray, depth=4)

    avg_samples_color = np.divide(pixel_color, global_camera.samples_per_pixel)
    return j, i, utils.write_color(avg_samples_color)

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
            samples_per_pixel:int = 12,
            fov:float = 90.0

        ) -> None:
        # Default data
        self.world = world
        self.width = width
        self.aspect_ratio = aspect_ratio
        self.center = center
        self.focal_length = focal_lenght
        self.look_at = look_at
        self.up = up
        self.fov = fov
        self.height:int = int(self.width / self.aspect_ratio)

        # Create pixel matrix
        self.pixels = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        # Sampling rate
        self.samples_per_pixel = samples_per_pixel
        self._pixel_samples_scale = 1.0 / self.samples_per_pixel

        # Calculate the orthonormal basis vectors for the camera orientation
        self.z_axis = utils.normalize(self.center - self.look_at)
        self.x_axis = utils.normalize(np.cross(self.up, self.z_axis))
        self.y_axis = np.cross(self.x_axis, self.z_axis)

        # Determine viewport dimensions based on fov
        theta:float = np.radians(self.fov)
        half_height:float = np.tan(theta / 2)
        # self.viewport_height:float = 2.0
        # self.viewport_width:float = self.viewport_height * (float(self.width) / self.height)
        self.viewport_height = 2.0 * half_height
        self.viewport_width = aspect_ratio * self.viewport_height

        # Calculate vector across the horizontal and down the vertical viewport edges
        self.viewport_u:np.ndarray = self.viewport_width * self.x_axis
        self.viewport_v:np.ndarray = self.viewport_height * self.y_axis

        # Calculate the horizontal and vertical delta vectors from pixel to pixel
        self.pixel_delta_u:np.ndarray = self.viewport_u / self.width
        self.pixel_delta_v:np.ndarray = self.viewport_v / self.height

        # Calculate location of upper left pixel
        self.viewport_upper_left:np.ndarray = self.center - (self.focal_length * self.z_axis) - self.viewport_u/2 - self.viewport_v/2

        self.pixel_00_location:np.ndarray = self.viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)


    def render(self, output_filepath="output.png") -> None:
        pixel_coords = [
            (i, j) for j in range(self.height) for i in range(self.width)
        ]

        with Pool(
                processes=cpu_count(), 
                initializer=_init_process, 
                initargs=(self,)
            ) as pool:

            results = pool.imap(_process_pixel, pixel_coords, chunksize=100)

            for result in tqdm(results, total=len(pixel_coords), desc="Rendering"):
                j, i, color = result
                self.pixels[j, i] = color

        image = Image.fromarray(self.pixels)
        image.save(output_filepath)


    def ray_color(self, ray:Ray, depth:int) -> np.ndarray:
        if depth <= 0:
            return colors.BLACK
        
        intersection:Hit | Light | None = self.world.get_nearest_hit(ray)

        if isinstance(intersection, Hit):
            return intersection.instance.material.eval(
                self.world, 
                intersection, 
                ray, 
                depth, 
                self
            )
        
        elif isinstance(intersection, Light):
            return intersection.color
        
        else:
            return colors.BLACK


    def sample_ray(self, pixel_i:int, pixel_j:int) -> Ray:
        """
        Generates a random ray with origin at the camera center and direction 
        to the surrounding of current pixel (i, j).
        
        The direction point is randomly chosen by a uniform distribution
        function.
        """
        offset:np.ndarray = utils.sample_square()

        pixel_sample:np.ndarray = (
            self.pixel_00_location
            + ((pixel_i + offset[0]) * self.pixel_delta_u)
            + ((pixel_j + offset[1]) * self.pixel_delta_v)
        )

        return Ray(self.center, utils.normalize(pixel_sample - self.center))

    