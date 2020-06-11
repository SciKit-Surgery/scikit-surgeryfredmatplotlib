#  -*- coding: utf-8 -*-

"""
Functions (in 2d) for point based registration using Orthogonal Procrustes.
"""

import math
import numpy as np
import sksurgerycore.algorithms.vector_math as vm


def compute_tre_from_fle_2d(fiducials, mean_fle_squared, target_point):
    """
    Computes an estimation of TRE from FLE and a list of fiducial locations.
    in 2d only

    See:
    `Fitzpatrick (1998), equation 46 <http://dx.doi.org/10.1109/42.736021>`_.

    :param fiducials: Nx3 ndarray of fiducial points
    :param mean_fle_squared: expected (mean) FLE squared
    :param target_point: a point for which to compute TRE.
    :return: mean TRE squared
    """
    # pylint: disable=literal-comparison

    dimension = 2
    if not isinstance(fiducials, np.ndarray):
        raise TypeError("fiducials is not a numpy array'")
    if not fiducials.shape[1] == dimension:
        raise ValueError("fiducials should have 2 columns")
    if fiducials.shape[0] < 3:
        raise ValueError("fiducials should have at least 3 rows")
    if not isinstance(target_point, np.ndarray):
        raise TypeError("target_point is not a numpy array'")
    if not target_point.shape[1] == dimension:
        raise ValueError("target_point should have 2 columns")
    if not target_point.shape[0] == 1:
        raise ValueError("target_point should have 1 row")

    number_of_fiducials = fiducials.shape[0]
    centroid = np.mean(fiducials, axis=0)
    covariance = np.cov(fiducials.T)
    assert covariance.shape[0] == dimension
    assert covariance.shape[1] == dimension
    _, eigen_vectors_matrix = np.linalg.eig(covariance)

    f_array = np.zeros(dimension)
    for axis_index in range(dimension):
        sum_f_k_squared = 0
        for fiducial_index in range(fiducials.shape[0]):
            f_k = vm.distance_from_line(centroid,
                                        eigen_vectors_matrix[axis_index],
                                        fiducials[fiducial_index])
            sum_f_k_squared = sum_f_k_squared + f_k * f_k
        f_k_rms = np.sqrt(sum_f_k_squared / number_of_fiducials)
        f_array[axis_index] = f_k_rms

    inner_sum = 0
    for axis_index in range(dimension):
        d_k = vm.distance_from_line(centroid,
                                    eigen_vectors_matrix[axis_index],
                                    target_point)
        inner_sum = inner_sum + (d_k * d_k / f_array[axis_index])

    mean_tre_squared = (mean_fle_squared / fiducials.shape[0]) * \
                       (1 + (1./float(dimension)) * inner_sum)
    return mean_tre_squared


def compute_fre_2d(fiducials, mean_fle_squared):
    """
    Equation 10 from
    `Fitzpatrick (1998), equation 46 <http://dx.doi.org/10.1109/42.736021>`_.
    from Sibson [23]
    """
    fre_sq = (1 - (2.0 / float(fiducials.shape[0]))) * mean_fle_squared

    return fre_sq


def expected_absolute_value(std_devs):
    """
    Returns the expected absolute value of a normal
    distribution with mean 0 and standard deviations std_dev
    see https://en.wikipedia.org/wiki/Folded_normal_distribution
    """

    #have we got the maths quite right here. fle is 1D,
    #mean_fle_squared if 2D? Check with a unit test
    if np.any(np.array(std_devs) < 0.0):
        raise ValueError("Cannot have negative standard deviation")

    std_dev_1d = np.linalg.norm(std_devs)
    return math.sqrt(2.0 / math.pi) * std_dev_1d
