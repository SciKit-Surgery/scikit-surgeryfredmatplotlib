"""Plotting functions for scikit-surgeryFRED
"""

import matplotlib.pyplot as plt

from sksurgeryfred.logging.fred_logger import Logger
def plot_results():
    """
    Plots the results  of multiple runs, from the log file.
    """

    log_config = {"logger" : {
        "log file name" : "fred_results.log",
        "overwrite existing" : False
        }}

    logger = Logger(log_config)

    [actual_tres, actual_fres, expected_tres, expected_fres,
     mean_fles, no_fids] = logger.read_log()

    _, subplot = plt.subplots(1, 5, figsize=(18, 8))

    subplot[0].scatter(actual_fres, actual_tres)
    subplot[1].scatter(expected_tres, actual_tres)
    subplot[2].scatter(expected_fres, actual_tres)
    subplot[3].scatter(mean_fles, actual_tres)
    subplot[4].scatter(no_fids, actual_tres)

    plt.show()
