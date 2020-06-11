# coding=utf-8

"""Fiducial Registration Educational Demonstration tests"""
import math
import numpy as np
import pytest
import sksurgeryfred.algorithms.errors_2d as e2d

# Pytest style

def _eav_by_brute_force(stddevs):

    cum_sum = np.zeros(np.array(stddevs).shape, dtype=np.float64)
    for _ in range(1000):
        cum_sum += np.absolute(np.random.normal(
            loc=np.zeros(np.array(stddevs).shape),
            scale=stddevs))

    eavs = cum_sum/1000.0
    eav = np.linalg.norm(eavs)

    return eav

def test_expected_absolute_value_1d():
    """
    Tests that expected absolute value works for the one dimensional case
    """
    np.random.seed(0)
    stddevs = np.array([0.0], dtype=np.float64)

    stddevs[0] = -1.0
    with pytest.raises(ValueError):
        eav = e2d.expected_absolute_value(stddevs)

    stddevs[0] = 0.0
    eav = e2d.expected_absolute_value(stddevs)

    assert eav == 0.0
    assert eav == _eav_by_brute_force(stddevs)

    stddevs[0] = 1.0
    eav = e2d.expected_absolute_value(stddevs)

    arith_eav = np.linalg.norm(stddevs) * math.sqrt(2.0/math.pi)
    assert np.isclose(eav, arith_eav, atol=0.0, rtol=0.0001)
    #absolute(a - b) <= (atol + rtol * absolute(b))
    #so rtol = 0.1 is around 10% rtol = 0.01 is 1 %
    assert np.isclose(eav, _eav_by_brute_force(stddevs), atol=0.0, rtol=0.05)

    for _ in range(10):
        stddevs[0] = np.absolute(np.random.normal()*100.0)
        eav = e2d.expected_absolute_value(stddevs)

        arith_eav = np.linalg.norm(stddevs) * math.sqrt(2.0/math.pi)
        assert np.isclose(eav, arith_eav, atol=0.0, rtol=0.0001)
        assert np.isclose(eav, _eav_by_brute_force(stddevs),
                          atol=0.0, rtol=0.05)


def test_expected_absolute_value_2d():
    """
    Tests that expected absolute value works for the two dimensional case
    """
    np.random.seed(0)
    stddevs = np.array([0.0, 0.0], dtype=np.float64)

    stddevs[1] = -1.0
    with pytest.raises(ValueError):
        eav = e2d.expected_absolute_value(stddevs)

    stddevs = [0.0, 0.0]
    eav = e2d.expected_absolute_value(stddevs)

    assert eav == 0.0
    assert eav == _eav_by_brute_force(stddevs)

    stddevs = [1.0, 1.0]
    eav = e2d.expected_absolute_value(stddevs)

    arith_eav = np.linalg.norm(stddevs) * math.sqrt(2.0/math.pi)
    assert np.isclose(eav, arith_eav, atol=0.0, rtol=0.0001)
    assert np.isclose(eav, _eav_by_brute_force(stddevs), atol=0.0, rtol=0.05)

    for _ in range(10):
        stddevs = np.absolute(np.random.normal((1, 1))*100.0)
        eav = e2d.expected_absolute_value(stddevs)
        arith_eav = np.linalg.norm(stddevs) * math.sqrt(2.0/math.pi)
        assert np.isclose(eav, arith_eav, atol=0.0, rtol=0.0001)
        assert np.isclose(eav, _eav_by_brute_force(stddevs),
                          atol=0.0, rtol=0.05)



def test_expected_absolute_value_3d():
    """
    Tests that expected absolute value works for the three dimensional case
    """
    np.random.seed(0)
    stddevs = np.array([0.0, 0.0, 0.0], dtype=np.float64)

    stddevs[1] = -1.0
    with pytest.raises(ValueError):
        eav = e2d.expected_absolute_value(stddevs)

    stddevs = [0.0, 0.0, 0.0]
    eav = e2d.expected_absolute_value(stddevs)

    assert eav == 0.0
    assert eav == _eav_by_brute_force(stddevs)

    stddevs = [1.0, 1.0, 1.0]
    eav = e2d.expected_absolute_value(stddevs)

    arith_eav = np.linalg.norm(stddevs) * math.sqrt(2.0/math.pi)
    assert np.isclose(eav, arith_eav, atol=0.0, rtol=0.0001)
    assert np.isclose(eav, _eav_by_brute_force(stddevs), atol=0.0, rtol=0.05)

    for _ in range(10):
        stddevs = np.absolute(np.random.normal((1, 1, 1))*100.0)
        eav = e2d.expected_absolute_value(stddevs)
        arith_eav = np.linalg.norm(stddevs) * math.sqrt(2.0/math.pi)
        assert np.isclose(eav, arith_eav, atol=0.0, rtol=0.0001)
        assert np.isclose(eav, _eav_by_brute_force(stddevs),
                          atol=0.0, rtol=0.05)
