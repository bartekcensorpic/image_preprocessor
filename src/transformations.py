from PIL import Image
from skimage.feature import hog
from skimage import exposure
import numpy as np
from enum import Enum
from skimage.restoration import denoise_tv_chambolle

class TransformationsEnum(Enum):
    grey_scale = 'grayscale'
    hog = 'hog'
    edge_enh = 'edge_enh'
    tv_den = 'tv_den'

    def __str__(self):
        return self.value

def to_gray_scale(image:Image.Image)-> Image.Image:
    """
    Transform image to grayscale

    :param image: image to be transformed (Pillow image)
    :return: grayscale image (Pillow image)
    """

    return image.convert('L')


def to_hog(image:Image.Image)-> Image.Image:

    pixels = np.array(image)
    fd, hog_image = hog(image, orientations=8, pixels_per_cell=(8, 8),
                        cells_per_block=(1, 1), visualize=True, multichannel=True)

    hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))

    return hog_image_rescaled

def edge_enhacement(image:Image.Image)-> Image.Image:
    from PIL import ImageFilter

    edgeEnahnced = image.filter(ImageFilter.EDGE_ENHANCE)

    return edgeEnahnced

def denoise_tv(image:Image.Image) -> Image.Image:

    pixels = np.array(image)
    denoised_img = denoise_tv_chambolle(pixels)
    img = Image.fromarray(np.uint8(denoised_img*255))
    return img

