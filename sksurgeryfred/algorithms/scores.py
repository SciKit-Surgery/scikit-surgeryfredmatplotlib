#  -*- coding: utf-8 -*-

"""
Functions for calculating the score for ablation game
"""

import math
import numpy as np


def sphere_volume(radius):
    """
    :returns: the volume of a sphere of radius
    """
    return 4.0 * math.pi * radius * radius * radius / 3.0

def two_sphere_overlap_volume(centre0, centre1, radius0, radius1):
    """
    Calculates the overlapping volume of two spheres
    :param: centre0 centre of sphere0 (1x3)
    :param: centre1 centre of sphere1 (1x3)
    :param: radius0 radius of sphere0 (1)
    :param: radius1 radius of sphere1 (1)
    """


    distance = np.linalg.norm(centre1 - centre0)

    sum_radii = radius0 + radius1
    abs_diff_radii = abs(radius0 - radius1)

    if distance >= sum_radii:
        return 0.0

    if distance < abs_diff_radii:
        if radius0 < radius1:
            return sphere_volume(radius0)
        return sphere_volume(radius1)

    first_term = math.pi / (12 * distance)
    second_term = (sum_radii - distance) * (sum_radii - distance)
    third_term = (distance * distance +
                  2 * distance * sum_radii -
                  3 * abs_diff_radii * abs_diff_radii)

    return first_term * second_term * third_term
