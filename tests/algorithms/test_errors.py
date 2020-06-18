# coding=utf-8

"""Fiducial Registration Educational Demonstration tests"""
import math
import numpy as np
import pytest

from sksurgerycore.algorithms.procrustes import orthogonal_procrustes
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


def test_compute_tre_from_fle_2d():
    """
    Tests for tre_from_fle_2d
    """

    stddevs = np.array([1.0, 1.0] , dtype=np.float64)
    mean_fle_squared = e2d.expected_absolute_value(stddevs)
    #three points on a unit circle
    angle0 = 0.0
    angle1 = math.pi * 2.0/3.0
    angle2 = math.pi * 4.0/3.0
    radius = 1.0

    fiducials = np.array([[radius * math.cos(angle0) , radius * math.sin(angle0)],
                          [radius * math.cos(angle1) , radius * math.sin(angle1)],
                          [radius * math.cos(angle2) , radius * math.sin(angle2)]])

    target = np.array([[0.0, 0.0, 0.0]])

    target_dist_from_principal_axis = [0.0, 0.0]
    rms_fiducial_dist_from_principal_x_axis = math.sqrt(
        (fiducials[0][0]*fiducials[0][0] + 
         fiducials[1][0]*fiducials[1][0] + 
         fiducials[2][0]*fiducials[2][0])/3.0)
    rms_fiducial_dist_from_principal_y_axis = math.sqrt(
        (fiducials[0][1]*fiducials[0][1] + 
         fiducials[1][1]*fiducials[1][1] + 
         fiducials[2][1]*fiducials[2][1])/3.0)

    moment_of_inerta = (target_dist_from_principal_axis[0] *
                        target_dist_from_principal_axis[0] /
                        (rms_fiducial_dist_from_principal_x_axis * 
                         rms_fiducial_dist_from_principal_x_axis) +
                        target_dist_from_principal_axis[1] *
                        target_dist_from_principal_axis[1] /
                        (rms_fiducial_dist_from_principal_y_axis *
                         rms_fiducial_dist_from_principal_y_axis))/2.0
    tre_squared = mean_fle_squared / float(fiducials.shape[1]) * ( 
        1.0 + moment_of_inerta)

    print (tre_squared)
    assert e2d.compute_tre_from_fle_2d(fiducials, mean_fle_squared, target[:, 0:2]) == tre_squared

    #next we try it with a brute force simulation
    rotation, translation, fre = orthogonal_procrustes(
                fixed_points, moving_points)
    
    transformed_target = np.matmul(rotation,
                                           target.transpose()) + \
                                           translation
    
    transformed_target_2d = [transformed_target[0][0],
                                     transformed_target[1][0]]

    actual_tre = np.linalg.norm(
                transformed_target_2d - self.target[:, 0:2])


def test_compute_tre_from_fle_2d_brute_force():
    """
    Tests for tre_from_fle_2d
    """

    stddevs = np.array([[1.0, 1.0, 0.0],[1.0, 1.0, 0.0],[1.0, 1.0, 0.0]] , dtype=np.float64)
    mean_fle_squared = e2d.expected_absolute_value(np.array([1.0,1.0]))
    #three points on a unit circle
    angle0 = 0.0
    angle1 = math.pi * 2.0/3.0
    angle2 = math.pi * 4.0/3.0
    radius = 1.0

    fiducials = np.array([[radius * math.cos(angle0) , radius * math.sin(angle0), 0.0],
                          [radius * math.cos(angle1) , 1.0 * math.sin(angle1), 0.0],
                          [radius * math.cos(angle2) , 1.0 * math.sin(angle2), 0.0]])

    print(fiducials)

    target = np.array([[0.0, 0.0, 0.0]])

    
    tre_sum = 0
    for _ in range (1000):
        moving_fids = fiducials
        fixed_fids = fiducials + np.random.normal(scale=stddevs)
        print (fixed_fids)
        print (moving_fids)
    #next we try it with a brute force simulation
        rotation, translation, fre = orthogonal_procrustes(
                fixed_fids, moving_fids)
    
        transformed_target = np.matmul(rotation,
                                       target.transpose()) + \
                                       translation
    
        transformed_target_2d = [transformed_target[0][0],
                                     transformed_target[1][0]]

        actual_tre = np.linalg.norm(
                transformed_target_2d - target[:, 0:2])
        
        tre_sum += actual_tre

    print (tre_sum/1000.0)
    print (e2d.compute_tre_from_fle_2d(fiducials[:,0:2], mean_fle_squared, target[:, 0:2]))
