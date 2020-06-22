# coding=utf-8

"""Fiducial Registration Educational Demonstration tests"""
import math
import numpy as np
import pytest

from sksurgerycore.algorithms.procrustes import orthogonal_procrustes
import sksurgeryfred.algorithms.fred as fred

def _eav_by_brute_force(stddevs):

    cum_sum = np.zeros(np.array(stddevs).shape, dtype=np.float64)
    for _ in range(1000):
            #cum_sum += np.absolute(np.random.normal(
        #    loc=np.zeros(np.array(stddevs).shape),
        #    scale=stddevs))

        cum_sum += np.random.normal(
            loc=np.zeros(np.array(stddevs).shape),
            scale=stddevs)

    eavs = cum_sum/1000.0
    eav = np.linalg.norm(eavs)
    print("brute eav = ", eav)
    return eav

def _easv_by_brute_force(stddevs):

    cum_sum = 0.0
    for _ in range(1000):
            #cum_sum += np.absolute(np.random.normal(
        #    loc=np.zeros(np.array(stddevs).shape),
        #    scale=stddevs))

        error = np.random.normal(
            loc=np.zeros(np.array(stddevs).shape),
            scale=stddevs)
        fre = np.linalg.norm(error)
        cum_sum += (fre * fre)

    easv = cum_sum/1000.0
    print("brute easv = ", easv)
    return easv

def _make_circle_fiducials(no_fids, centre, radius, 
                           fixed_stddevs, moving_stddevs):

    fixed_fids = np.zeros(shape = (no_fids, 3), dtype = np.float64)
    moving_fids = np.zeros(shape = (no_fids, 3), dtype = np.float64)

    angle_inc = math.pi * 2.0 / float(no_fids)
    
    for fid in range(no_fids):
        fixed_fids[fid] = ([radius * math.cos(angle_inc*fid),
                            radius * math.sin(angle_inc*fid),
                            0.0] + 
                            np.random.normal(scale=fixed_stddevs) +
                            centre)

        moving_fids[fid] = ([radius * math.cos(angle_inc*fid),
                            radius * math.sin(angle_inc*fid),
                            0.0] + 
                            np.random.normal(scale=moving_stddevs) +
                            centre)
                   
    return fixed_fids, moving_fids


def test_point_based_registration_3_fids():
    """
    Tests for tre_from_fle_2d
    """
    
    fixed_fle_std_dev = np.array([1.0, 1.0, 0.0], dtype=np.float64)
    moving_fle_std_dev = np.array([0.0, 0.0, 0.0], dtype=np.float64)

    fixed_fle_easv = _easv_by_brute_force(fixed_fle_std_dev)
    moving_fle_easv = _easv_by_brute_force(moving_fle_std_dev)
   
    target = np.array([[0.0, 0.0, 0.0]], dtype=np.float64)

    pbr = fred.PointBasedRegistration(target, fixed_fle_easv, moving_fle_easv)
    
    centre = np.array([0.0, 0.0, 0.0], dtype=np.float64)
    radius = 2.0

    tresq_sum = 0
    fresq_sum = 0
    expected_tre_squared = 0
    expected_fre = 0
    repeats = 1000
    for _ in range(repeats):
        fixed_fids, moving_fids = _make_circle_fiducials(3, centre, radius, 
                                                         fixed_fle_std_dev,
                                                         moving_fle_std_dev)


        [success, fre, mean_fle, expected_tre_squared, expected_fre,
            transformed_target_2d, actual_tre, no_fids] = pbr.register(
                fixed_fids, moving_fids)
        
        tresq_sum += actual_tre*actual_tre
        fresq_sum += fre*fre

    ave_tresq = tresq_sum/repeats
    ave_fresq = fresq_sum/repeats

    print ("Exp TRE, actual ", expected_tre_squared, ave_tresq)
    print ("Exp FRE, actual ", expected_fre, ave_fresq)

def test_point_based_registration_10_fids():
    """
    Tests for tre_from_fle_2d
    """
    
    fixed_fle_std_dev = np.array([1.0, 1.0, 0.0], dtype=np.float64)
    moving_fle_std_dev = np.array([0.0, 0.0, 0.0], dtype=np.float64)

    fixed_fle_easv = _easv_by_brute_force(fixed_fle_std_dev)
    moving_fle_easv = _easv_by_brute_force(moving_fle_std_dev)
   
    target = np.array([[0.0, 0.0, 0.0]], dtype=np.float64)

    pbr = fred.PointBasedRegistration(target, fixed_fle_easv, moving_fle_easv)
    
    centre = np.array([0.0, 0.0, 0.0], dtype=np.float64)
    radius = 2.0

    tresq_sum = 0
    fresq_sum = 0
    expected_tre_squared = 0
    expected_fre = 0
    repeats = 1000
    for _ in range(repeats):
        fixed_fids, moving_fids = _make_circle_fiducials(10, centre, radius, 
                                                         fixed_fle_std_dev,
                                                         moving_fle_std_dev)


        [success, fre, mean_fle, expected_tre_squared, expected_fre,
            transformed_target_2d, actual_tre, no_fids] = pbr.register(
                fixed_fids, moving_fids)
        
        tresq_sum += actual_tre*actual_tre
        fresq_sum += fre*fre

    ave_tresq = tresq_sum/repeats
    ave_fresq = fresq_sum/repeats

    print ("10 fids: Exp TRE, actual ", expected_tre_squared, ave_tresq)
    print ("10 fids: Exp FRE, actual ", expected_fre, ave_fresq)

def test_point_based_registration_10_fids_offset_target():
    """
    Tests for tre_from_fle_2d
    """
    
    fixed_fle_std_dev = np.array([1.0, 1.0, 0.0], dtype=np.float64)
    moving_fle_std_dev = np.array([0.0, 0.0, 0.0], dtype=np.float64)

    fixed_fle_easv = _easv_by_brute_force(fixed_fle_std_dev)
    moving_fle_easv = _easv_by_brute_force(moving_fle_std_dev)
   
    target = np.array([[2.0, 1.0, 0.0]], dtype=np.float64)

    pbr = fred.PointBasedRegistration(target, fixed_fle_easv, moving_fle_easv)
    
    centre = np.array([0.0, 0.0, 0.0], dtype=np.float64)
    radius = 2.0

    tresq_sum = 0
    fresq_sum = 0
    expected_tre_squared = 0
    expected_fre = 0
    repeats = 1000
    for _ in range(repeats):
        fixed_fids, moving_fids = _make_circle_fiducials(10, centre, radius, 
                                                         fixed_fle_std_dev,
                                                         moving_fle_std_dev)


        [success, fre, mean_fle, expected_tre_squared, expected_fre,
            transformed_target_2d, actual_tre, no_fids] = pbr.register(
                fixed_fids, moving_fids)
        
        tresq_sum += actual_tre*actual_tre
        fresq_sum += fre*fre

    ave_tresq = tresq_sum/repeats
    ave_fresq = fresq_sum/repeats

    print ("10 fids offset: Exp TRE, actual ", expected_tre_squared, ave_tresq)
    print ("10 fids offset: Exp FRE, actual ", expected_fre, ave_fresq)

