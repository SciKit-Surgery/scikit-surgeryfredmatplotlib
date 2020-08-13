# coding=utf-8

"""Fiducial Registration Educational Demonstration tests"""
import numpy as np

from sksurgeryfred.widgets.interactive_registration \
                import InteractiveRegistration as ireg 


def test_int_reg():
    int_reg = ireg('data/brain512.png', headless=True)
