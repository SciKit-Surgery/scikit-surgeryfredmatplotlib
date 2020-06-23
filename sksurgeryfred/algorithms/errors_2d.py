#  -*- coding: utf-8 -*-

"""
Functions (in 2d) for point based registration using Orthogonal Procrustes.
"""

import math
import numpy as np
import sksurgerycore.algorithms.vector_math as vm


def expected_absolute_value(std_devs):
    """
    Returns the expected absolute value of a normal
    distribution with mean 0 and standard deviations std_dev
    """

    onedsd = np.linalg.norm(std_devs)
    variance = onedsd * onedsd
    return variance
