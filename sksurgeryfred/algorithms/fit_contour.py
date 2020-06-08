

from skimage.color import rgb2gray
from skimage import data
from skimage.filters import gaussian
from skimage.segmentation import active_contour
from skimage.io import imread

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def find_outer_contour(image, alpha=0.015, beta=10.0):
    """
    Fits an active contour to the outer most edge in the image
    :params image: the image to fit to
    :params alpha: Snake length shape parameter. Higher values makes snake contract
        faster (default 0.15)
    :params beta: Snake smoothness shape parameter. Higher values makes snake 
        smoother (default 10.0)
    :returns: the resulting contour and the initialising contour
    """

    image = to_gray(image)

    centre = np.array([image.shape[0], image.shape[1]])/2.0
    radius = np.array([image.shape[0], image.shape[1]])/2.0

    s = np.linspace(0, 2*np.pi, 400)
    r = centre[0] + radius[0]*np.sin(s)
    c = centre[1] + radius[1]*np.cos(s)
    init = np.array([r, c]).T

    snake = active_contour(gaussian(image, 3),
                           init, alpha, beta, gamma=0.001,
                           coordinates='rc')
    return snake, init


def to_gray(image):
    """
    converts and image to grayscale if not already done
    :params image: The image to convert, can be gray or rgb
    :returns: a grayscale version
    """

    if image.ndim == 2:
        return image
    else:
        return rgb2gray(image)

