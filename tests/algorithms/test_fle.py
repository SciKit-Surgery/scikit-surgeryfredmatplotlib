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
    ind_fle_function = None
    systematic_fle = 0.0
    sys_fle_function = None
    dimension = 3
    _fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                     sys_fle_function, dimension)

    #test we can init with an array
    systematic_fle = np.full(1, 2.0, dtype=np.float64)
    independent_fle = np.full(2, 2.0, dtype=np.float64)
    dimension = 2
    _fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                     sys_fle_function, dimension)

    #test we get a value error if the array is the wrong size
    systematic_fle = np.full(3, 2.0, dtype=np.float64)

    with pytest.raises(ValueError):
        _fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                         sys_fle_function, dimension)

    #test we can pass our own function
    def my_add():
        return np.full(2, 2.0, dtype=np.float64)

    systematic_fle = None
    sys_fle_function = my_add
    _fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                     sys_fle_function, dimension)

    #test we get value error when we set both function and value
    systematic_fle = 1.0
    with pytest.raises(ValueError):
        _fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                         sys_fle_function, dimension)
    ind_fle_function = my_add
    with pytest.raises(ValueError):
        _fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                         sys_fle_function, dimension)

    #test we get type errors if the function is wrong
    def my_bad_add(array_a):
        return array_a

    sys_fle_function = my_bad_add
    systematic_fle = None
    ind_fle_function = None
    with pytest.raises(TypeError):
        _fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                         sys_fle_function, dimension)
    ind_fle_function = my_bad_add
    independent_fle = None
    with pytest.raises(TypeError):
        _fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                         sys_fle_function, dimension)
