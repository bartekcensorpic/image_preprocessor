from PIL import Image
from skimage.feature import hog
from skimage import exposure
import numpy as np
from enum import Enum

class TransformationsEnum(Enum):
    grey_scale = 'grayscale'
    hog = 'hog'

    def __str__(self):
        return self.value

def to_gray_scale(image:Image.Image)-> Image.Image:
    """
    Transform image to grayscale

    :param image: image to be transformed (Pillow image)
    :return: grayscale image (Pillow image)
    """

    return image.convert('L')


def to_hog(image:Image.Image)-> np.ndarray:
    """
    transforms image using histogram of oriented gradients

    :param image: image to be transformed (Pillow image)
    :return: np.array
    """

    pixels = np.array(image)
    fd, hog_image = hog(image, orientations=8, pixels_per_cell=(8, 8),
                        cells_per_block=(1, 1), visualize=True, multichannel=True)

    hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))

    return hog_image_rescaled
