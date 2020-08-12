# coding=utf-8

"""Fiducial Registration Educational Demonstration tests"""
import numpy as np

from sksurgeryfred.algorithms.fle import FLE

def test_fle_init():
    """Tests for FLE init"""

    #test default works
    _fixed_fle = FLE()

    #test we can init with single value FLE
    independent_fle = 1.0
    ind_fle_function = np.random.uniform
    systematic_fle = 0.0
    sys_fle_function = np.add
    dimension = 3
    fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                    sys_fle_function, dimension)

    assert np.array_equal(fixed_fle.ind_fle, np.full(dimension, 1.0,
                                                     dtype=np.float64))
    assert np.array_equal(fixed_fle.sys_fle, np.zeros(dimension,
                                                      dtype=np.float64))

    systematic_fle = np.full(1, 2.0, dtype=np.float64)
    independent_fle = 0.0
    dimension = 2
    fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                    sys_fle_function, dimension)

    assert np.array_equal(fixed_fle.sys_fle, np.full(dimension, 2.0,
                                                     dtype=np.float64))
    assert np.array_equal(fixed_fle.ind_fle, np.zeros(dimension,
                                                      dtype=np.float64))
