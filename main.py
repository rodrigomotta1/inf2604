import numpy as np

from camera import Camera
from scenes import balls, cornell_box



def main():
    
    camera = Camera(
        world=cornell_box,
        center=np.array([2.775, 3.2, 12.775]),
        look_at=np.array([2.775, 2.775, 2.775]),
        fov=50
    )

    camera.render()


if __name__ == "__main__":
    main()