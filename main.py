import numpy as np
import time

from tqdm import tqdm
from PIL import Image
from utils import write_color


def main():
    # Image
    image_width:int = 256
    image_height:int = 256

    _t_iter:int = image_height * image_width

    # Render
    pixels = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    # Progress
    _progress_bar = tqdm(total=_t_iter, desc="Progress", unit="iter")

    for j in range(0, image_height):
        for i in range(0, image_width):
            r:float = float(i) / (image_width - 1)
            g:float = float(j) / (image_height - 1)
            b:float = 0

            color:np.ndarray = write_color(np.array([r, g, b]))
            # print(color)

            pixels[j, i] = color

            _progress_bar.update(1)

    image = Image.fromarray(pixels)
    image.save("output.png")
    # print(f"\nDone")
    # image.show()


if __name__ == "__main__":
    main()