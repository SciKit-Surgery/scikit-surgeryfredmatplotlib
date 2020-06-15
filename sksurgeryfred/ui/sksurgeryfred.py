# coding=utf-8

"""User interfaces for sksurgeryFRED"""

from sksurgeryfred.algorithms.fred import \
                plot_errors_interactive, make_target_point

def run_demo(image):
    """Run FRED"""

    target = make_target_point()
    plot_errors_interactive(image, target)
