# coding=utf-8

"""Fiducial Registration Educational Demonstration tests"""
import numpy as np
import pytest

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

    #test we can init with an array
    systematic_fle = np.full(1, 2.0, dtype=np.float64)
    independent_fle = 0.0
    dimension = 2
    fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                    sys_fle_function, dimension)

    assert np.array_equal(fixed_fle.sys_fle, np.full(dimension, 2.0,
                                                     dtype=np.float64))
    assert np.array_equal(fixed_fle.ind_fle, np.zeros(dimension,
                                                      dtype=np.float64))


    #test we get a value error if the array is the wrong size
    systematic_fle = np.full(3, 2.0, dtype=np.float64)

    with pytest.raises(ValueError):
        fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                        sys_fle_function, dimension)

    #test we can pass our own function
    def my_add(array_a, array_b):
        return array_a + array_b

    systematic_fle = np.full(2, 2.0, dtype=np.float64)
    sys_fle_function = my_add
    fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                    sys_fle_function, dimension)

    #test we get type errors if the function is wrong
    def my_bad_add(array_a):
        return array_a

    systematic_fle = np.full(2, 2.0, dtype=np.float64)
    sys_fle_function = my_bad_add
    with pytest.raises(TypeError):
        fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                        sys_fle_function, dimension)
    ind_fle_function = my_bad_add
    with pytest.raises(TypeError):
        fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                        sys_fle_function, dimension)
