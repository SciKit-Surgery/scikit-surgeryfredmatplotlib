"""
The main widget for the interactive registration part of scikit-surgeryFRED
"""

import matplotlib.pyplot as plt

from sksurgeryfredbe.logging.fred_logger import Logger
from sksurgeryfred.widgets.fred_common import FredCommon

class InteractiveRegistration(FredCommon):
    """
    an interactive window for doing live registration
    """

    def __init__(self, image_file_name, headless=False):
        """
        Creates a visualisation of the projected and
        detected screen points, which you can click on
        to measure distances
        """
        super().__init__(image_file_name, headless)
        self.stats_plot.set_visibilities(True, True, True, True, True,
                                         False, False, False, False)

        self.plotter.show_actual_positions = True

        log_config = {"logger" : {
            "log file name" : "fred_results.log",
            "overwrite existing" : False
            }}

        self.logger = Logger(log_config)

        self.initialise_registration()

        _ = self.fig.canvas.mpl_connect('key_press_event',
                                        self.keypress_event)

        plt.show()

    def keypress_event(self, event):
        """
        handle a key press event
        """
        if event.key == 'r':
            self.initialise_registration()

    def initialise_registration(self):
        """
        sets up the registration
        """
        super().init_reg()
        self.fig.canvas.draw()
