# coding=utf-8

"""Fiducial Registration Educational Demonstration tests"""
import numpy as np

from sksurgeryfred.algorithms.fle import FLE

def test_fle_default():
    """Test fle init's with defaults"""

    fixed_fle = FLE()
