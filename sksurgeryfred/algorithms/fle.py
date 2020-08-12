#  -*- coding: utf-8 -*-

"""
Functions for adding fiducial localisation error
"""

import numpy as np


def _set_fle(fle, dims):
    """ Internal function to check and set the fle """
    if isinstance(fle, np.ndarray):
        if fle.size == 1:
            fle_array = np.full(dims, fle.item(0), dtype=np.float64)
        else:
            if fle.size != dims:
                raise ValueError("FLE value must be single value or array",
                                 " of length ", dims)
    else:
        fle_array = np.full(dims, fle, dtype=np.float64)

    assert fle_array.size == dims
    return fle_array

class FLE:
    """
    Provides methods to add Fiducial Localisation Error to a point

    :params independent_fle: the magnitude(s) of the independent FLE's,
        passed to the ind_fle_function, defaults to zero. A single float
        will yield isotropic error, or an array can be passed for
        anisotropic errors.
    :params ind_fle_function: the function to use for sampling the independent
        fle. Defaults to numpy.random.normal
    :params systematic_fle: the magnitude(s) of the systematic FLE's,
        passed to the sys_fle_function, defaults to zero. A single float
        will yield isotropic error, or an array can be passed for
        anisotropic errors.
    :params sys_fle_function: the function to use for sampling the independent
        fle. Defaults to numpy.add
    :params dimension: the dimensions to use, defaults to 3.

    :raises ValueError: If independent_fle is not single value or array of
        length dimension.
    :raises AttributeError: If either error function is invalid.


    """

    def __init__(self, independent_fle=0.0, ind_fle_function=np.random.normal,
                 systematic_fle=0.0, sys_fle_function=np.add, dimension=3):

        self.ind_fle = _set_fle(independent_fle, dimension)
        self.ind_fle_function = ind_fle_function

        try:
            self.ind_fle_function(self.ind_fle, self.ind_fle)
        except AttributeError:
            raise AttributeError("Failed to run function, ", ind_fle_function,
                                 "check name")

        self.sys_fle = _set_fle(systematic_fle, dimension)

        self.sys_fle_function = sys_fle_function

        try:
            self.sys_fle_function(self.sys_fle, self.sys_fle)
        except AttributeError:
            raise AttributeError("Failed to run function, ", sys_fle_function,
                                 "check name")


def add_guassian_fle_to_fiducial(fiducial, fle_standard_deviation):
    """Not in use"""
    #moved = np.random.normal(fiducial, fle_standard_deviation)
    uni_error = np.random.uniform(-fle_standard_deviation,
                                  fle_standard_deviation, (1, 3))
    return fiducial + uni_error
