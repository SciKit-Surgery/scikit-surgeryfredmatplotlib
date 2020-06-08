# coding=utf-8

"""Fiducial Registration Educational Demonstration tests"""
from numpy import array
from sksurgeryfred.ui.sksurgeryfred import run_demo

# Pytest style

def test_using_pytest_sksurgeryfred():

    run_demo("data/75yo_male.png") 


