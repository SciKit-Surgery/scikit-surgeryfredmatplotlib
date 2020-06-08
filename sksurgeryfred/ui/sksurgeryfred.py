# coding=utf-8

"""User interfaces for sksurgeryFRED"""

from numpy import array
from sksurgeryfred.algorithms.camera_calibration import \
                plot_errors_interactive

def run_demo(image):
    """Run FRED"""

    projpoint = array([[100, 100, 100]])
    plot_errors_interactive(image, projpoint, False)
