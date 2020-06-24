"""
The main widget for the interactive registration part of scikit-surgeryFRED
"""

import matplotlib.pyplot as plt
import skimage.io
import numpy as np

from sksurgeryfred.algorithms.fred import make_target_point, \
                AddFiducialMarker
from sksurgeryfred.plotting.interactive_plots import PlotRegistrations, \
                PlotRegStatistics
from sksurgeryfred.algorithms.point_based_reg import PointBasedRegistration
from sksurgeryfred.algorithms.fit_contour import find_outer_contour
from sksurgeryfred.algorithms.errors import expected_absolute_value
from sksurgeryfred.algorithms.ablation import Ablator
from sksurgeryfred.logging.fred_logger import Logger

class RegistrationGame:
    """
    an interactive window for doing live registration
    """

    def __init__(self, image_file_name):
        """
        Creates a visualisation of the projected and
        detected screen points, which you can click on
        to measure distances
        """

        self.fig, subplot = plt.subplots(1, 2, figsize=(20, 10))
        self.fig.canvas.set_window_title('SciKit-SurgeryF.R.E.D.')
        self.stats_plot = PlotRegStatistics(subplot[1])
        self.stats_plot.set_visibilities(True, True, False, False,
                                         True, True, True)

        self.total_score = 0
        self.repeats = 0
        self.stats_plot.update_last_score(0)
        self.stats_plot.update_total_score(self.total_score)

        self.plotter = PlotRegistrations(subplot[1], subplot[0],
                                         self.stats_plot)

        self.plotter.show_actual_positions = True

        log_config = {"logger" : {
            "log file name" : "fred_results.log",
            "overwrite existing" : False
            }}

        self.logger = Logger(log_config)
        self.mouse_int = None
        self.pbr = None
        self.image_file_name = image_file_name
        self.ablation = Ablator()

        self.intialise_registration()

        _ = self.fig.canvas.mpl_connect('key_press_event',
                                        self.keypress_event)

        plt.show()

    def keypress_event(self, event):
        """
        handle a key press event
        """
        if event.key == 'r':
            self.intialise_registration()

        if event.key == "up":
            margin = self.ablation.increase_margin()
            self.stats_plot.update_margin_stats(margin)
            self.fig.canvas.draw()

        if event.key == "down":
            margin = self.ablation.decrease_margin()
            self.stats_plot.update_margin_stats(margin)
            self.fig.canvas.draw()

        if event.key == "a":
            reg_ok, est_target = self.pbr.get_transformed_target()
            if reg_ok:
                score = self.ablation.ablate(est_target)
                if score is not None:
                    self.stats_plot.update_last_score(score)
                    self.total_score += score
                    self.stats_plot.update_total_score(self.total_score)
                    self.fig.canvas.draw()

    def intialise_registration(self):
        """
        sets up the registration
        """
        img = skimage.io.imread(self.image_file_name)
        outline, _initial_guess = find_outer_contour(img)
        target_point = make_target_point(outline)

        self.plotter.initialise_new_reg(img, target_point, outline)

        fle_sd = np.random.uniform(low=0.5, high=5.0)
        moving_fle = np.zeros((1, 3), dtype=np.float64)

        fixed_fle = np.array([fle_sd, fle_sd, fle_sd], dtype=np.float64)
        fixed_fle_eavs = expected_absolute_value(fixed_fle)
        moving_fle_eavs = expected_absolute_value(moving_fle)

        if self.pbr is None:
            self.pbr = PointBasedRegistration(target_point, fixed_fle_eavs,
                                              moving_fle_eavs)
        else:
            self.pbr.reinit(target_point, fixed_fle_eavs, moving_fle_eavs)

        if self.mouse_int is None:
            self.mouse_int = AddFiducialMarker(self.fig, self.plotter,
                                               self.pbr, self.logger,
                                               fixed_fle, moving_fle)

        self.mouse_int.reset_fiducials(fixed_fle_eavs)

        self.ablation.setup(margin=1.0, target=target_point,
                            target_radius=10.0)

        self.stats_plot.update_margin_stats(1.0)

        self.fig.canvas.draw()
