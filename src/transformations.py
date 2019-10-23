from PIL import Image
from skimage.feature import hog
import numpy as np
from enum import Enum

class TransformationsEnum(Enum):
    grey_scale = 'greyscale'
    hog = 'hog'

    def __str__(self):
        return self.value

def to_grey_scale(image:Image.Image)-> Image.Image:
    """
    Transform image to greyscale

    :param image: image to be transformed (Pillow image)
    :return: greyscale image (Pillow image)
    """

    return image.convert('L')


def to_hog(image:Image.Image)-> Image.Image:
    """
    transforms image using histogram of oriented gradients

    :param image: image to be transformed (Pillow image)
    :return: image (Pillow image)
    """

    pixels = np.array(image)
    fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16),
                        cells_per_block=(1, 1), visualize=True, multichannel=True)

    image_back = Image.fromarray(hog_image)

    return image_back