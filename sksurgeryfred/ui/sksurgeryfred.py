# coding=utf-8

"""User interfaces for sksurgeryFRED"""

from sksurgeryfred.algorithms.fred import InteractiveRegistration

def run_demo(image):
    """Run FRED"""

    InteractiveRegistration(image)
