# coding=utf-8

"""User interfaces for sksurgeryFRED"""

from sksurgeryfredmatplotlib.plotting.plotting import \
                plot_results

def run_plotter(logfile):
    """Run FRED Plotter"""

    plot_results(logfile)
