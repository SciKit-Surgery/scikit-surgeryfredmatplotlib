#  -*- coding: utf-8 -*-

"""
Functions for adding fiducial localisation error
"""

import numpy as np


def _set_fle(fle, dims):
    """ Internal function to check and set the fle """
    if fle is None:
        fle_array = np.full(3, 0.0, dtype=np.float64)
    else:
        if isinstance(fle, np.ndarray):
            if fle.size == 1:
                fle_array = np.full(3, fle.item(0), dtype=np.float64)
            else:
                if fle.size != dims:
                    raise ValueError("FLE value must be single value or array",
                                     " of length ", dims)
        else:
            fle_array = np.full(3, fle.item(0), dtype=np.float64)

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
        fle. Defaults to numpy

    :raises ValueError: If independent_fle is not single value or array of
        length 3

    """

    def __init__(self, independent_fle=None, ind_fle_function=None,
                 systematic_fle=None, sys_fle_function=None):

        self.dims = 3
        self.ind_fle = _set_fle(independent_fle, self.dims)
        if ind_fle_function is None:
            self.ind_fle_function = np.random.uniform

        try:
            self.ind_fle_function(self.ind_fle, self.ind_fle)
        except AttributeError:
            raise ValueError("Failed to run function, ", ind_fle_function,
                             "check name")


def add_guassian_fle_to_fiducial(fiducial, fle_standard_deviation):
    """Not in use"""
    #moved = np.random.normal(fiducial, fle_standard_deviation)
    uni_error = np.random.uniform(-fle_standard_deviation,
                                  fle_standard_deviation, (1, 3))
    return fiducial + uni_error
