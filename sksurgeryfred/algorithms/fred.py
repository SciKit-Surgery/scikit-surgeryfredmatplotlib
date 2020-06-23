"""Functions to support MedPhys Taught Module workshop on
calibration and tracking
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import skimage.io

from sksurgerycore.algorithms.procrustes import orthogonal_procrustes
from sksurgerycore.algorithms.errors import compute_tre_from_fle, compute_fre_from_fle

from sksurgeryfred.algorithms.fit_contour import find_outer_contour
from sksurgeryfred.algorithms.errors_2d import expected_absolute_value

from sksurgeryfred.logging.fred_logger import Logger

class PointBasedRegistration:
    """
    Does the registration and assoctiated measures
    """

    def __init__(self, target, fixed_fle_esv, moving_fle_esv):
        """
        :params target: 1x3 target point
        :params fixed_fle_esv: the expected squared value of the fixed image fle
        :params moving_fle_esv: the expected squared value of the moving image fle
        """
        if not moving_fle_esv == 0.0:
            raise NotImplementedError("Currently we only support zero fle on moving image ")

        self.target = None
        self.fixed_fle_esv = None
        self.moving_fle_esv = None
        self.reinit(target, fixed_fle_esv, moving_fle_esv)

    def reinit(self, target, fixed_fle_esv, moving_fle_esv):
        """
        reinitiatilses the target and errors
        """
        self.target = target
        self.fixed_fle_esv = fixed_fle_esv
        self.moving_fle_esv = moving_fle_esv

    def register(self, fixed_points, moving_points):
        """
        Does the registration
        """
        success = False
        fre = 0.0
        expected_tre = 0.0
        expected_fre_sq = 0.0
        actual_tre = 0.0

        no_fids = fixed_points.shape[0]

        if no_fids > 2:
            rotation, translation, fre = orthogonal_procrustes(
                fixed_points, moving_points)
            expected_tre_squared = compute_tre_from_fle(
                moving_points[:, 0:3],
                self.fixed_fle_esv,
                self.target[:, 0:3])
            expected_fre_sq = compute_fre_from_fle(moving_points[:, 0:3],
                               self.fixed_fle_esv)

            transformed_target = np.matmul(rotation,
                                           self.target.transpose()) + \
                                           translation
            actual_tre = np.linalg.norm(
                transformed_target - self.target[:, 0:3].transpose())
            #print("target =", self.target)
            #print("t_target = ", transformed_target)
            #print("difference =", transformed_target - self.target[:, 0:3].transpose())
            #print("tre = ", actual_tre)
            success = True


        return [success, fre, self.fixed_fle_esv, expected_tre_squared, expected_fre_sq,
                transformed_target[:, 0:3], actual_tre, no_fids]


class PlotRegStatistics():
    """
    writes the registration statistics
    """
    def __init__(self, plot):
        """
        The plot to write on
        """
        self.plot = plot
        self.fids_text = None
        self.tre_text = None
        self.exp_tre_text = None
        self.fre_text = None

        self.props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)



    def update_stats_plot(self, tre, exp_tre, fre, exp_fre):
        """
        Updates the statistics display
        """
        if self.tre_text is not None:
            self.tre_text.remove()
        if self.exp_tre_text is not None:
            self.exp_tre_text.remove()
        if self.fre_text is not None:
            self.fre_text.remove()

        stats_str = ('Expected FRE = {0:.2f}\n'.format(exp_fre) +
                     'Expected TRE = {0:.2f}'.format(exp_tre))

        actual_tre_str = ('Actual TRE = {0:.2f}'.format(tre))
        actual_fre_str = ('Actual FRE = {0:.2f}'.format(fre))

        self.exp_tre_text = self.plot.text(-1.05, 1.10, stats_str,
                                           transform=self.plot.transAxes,
                                           fontsize=26,
                                           verticalalignment='top',
                                           bbox=self.props)

        self.tre_text = self.plot.text(-0.1, 1.10, actual_tre_str,
                                       transform=self.plot.transAxes,
                                       fontsize=26,
                                       verticalalignment='top', bbox=self.props)

        self.fre_text = self.plot.text(0.65, 1.10, actual_fre_str,
                                       transform=self.plot.transAxes,
                                       fontsize=26,
                                       verticalalignment='top', bbox=self.props)


    def update_fids_stats(self, no_fids, mean_fle):
        """
        Updates the fids stats display
        """
        if self.fids_text is not None:
            self.fids_text.remove()

        fids_str = ('Number of fids = {0:}\n'.format(no_fids) +
                    'Expected FLE = {0:.2f}'.format(mean_fle))

        self.fids_text = self.plot.text(-1.95, 1.10, fids_str,
                                        transform=self.plot.transAxes,
                                        fontsize=26,
                                        verticalalignment='top',
                                        bbox=self.props)



class PlotRegistrations():
    """
    Plots the results of registrations
    """

    def __init__(self, fixed_plot, moving_plot):
        """
        :params fixed_plot: the fixed image subplot
        :params moving_plot: the moving image subplot
        """

        self.fixed_plot = fixed_plot
        self.moving_plot = moving_plot

        self.target_scatter = None
        self.trans_target_plots = [None, None]
        self.fixed_fids_plots = [None, None]
        self.moving_fids_plot = None

        self.stats_plot = PlotRegStatistics(fixed_plot)

        self.show_actual_positions = True
        self.target_point = None

    def initialise_new_reg(self, img, target_point, outline):
        """
        resets the registration
        """
        self.moving_plot.imshow(img)
        self.fixed_plot.plot(outline[:, 1], outline[:, 0], '-b', lw=3)
        self.fixed_plot.set_ylim([0, img.shape[0]])
        self.fixed_plot.set_xlim([0, img.shape[1]])
        self.fixed_plot.axis([0, img.shape[1], img.shape[0], 0])
        self.fixed_plot.axis('scaled')
        self.target_point = target_point

        if self.target_scatter is not None:
            self.target_scatter.remove()

        self.target_scatter = self.moving_plot.scatter(self.target_point[0, 0],
                                                       self.target_point[0, 1],
                                                       s=144, c='r')
        if self.trans_target_plots[0] is not None:
            self.trans_target_plots[0].remove()
            self.trans_target_plots[0] = None

        if self.trans_target_plots[1] is not None:
            self.trans_target_plots[1].remove()
            self.trans_target_plots[1] = None

        self.stats_plot.update_stats_plot(0, 0, 0, 0)

        self.moving_plot.set_title('Pre-Operative Image', y=-0.10,
                                   fontsize=26)
        self.fixed_plot.set_title('Patient in Theatre', y=-0.10,
                                  fontsize=26)


    def plot_fiducials(self, fixed_points, moving_points, no_fids, mean_fle):
        """
        Updates plot with fiducial data
        """

        if self.fixed_fids_plots[0] is not None:
            self.fixed_fids_plots[0].remove()
        if self.moving_fids_plot is not None:
            self.moving_fids_plot.remove()

        if self.fixed_fids_plots[1] is not None:
            self.fixed_fids_plots[1].remove()


        self.fixed_fids_plots[0] = self.fixed_plot.scatter(fixed_points[:, 0],
                                                           fixed_points[:, 1],
                                                           s=64, c='g',
                                                           marker='o')
        self.moving_fids_plot = self.moving_plot.scatter(moving_points[:, 0],
                                                         moving_points[:, 1],
                                                         s=64, c='g',
                                                         marker="o")

        if self.show_actual_positions:
            self.fixed_fids_plots[1] = self.fixed_plot.scatter(
                moving_points[:, 0],
                moving_points[:, 1],
                s=36, c='black',
                marker='+')

        self.stats_plot.update_fids_stats(no_fids, mean_fle)

    def plot_registration_result(self, actual_tre, expected_tre,
                                 fre, expected_fre, transformed_target_2d):
        """
        Plots the results of a registration
        """

        self.stats_plot.update_stats_plot(actual_tre, expected_tre,
                                          fre, expected_fre)


        if self.trans_target_plots[0] is not None:
            self.trans_target_plots[0].remove()

        if self.trans_target_plots[1] is not None:
            self.trans_target_plots[1].remove()

        self.trans_target_plots[0] = self.fixed_plot.scatter(
            transformed_target_2d[0],
            transformed_target_2d[1],
            s=144, c='r', marker='o')

        if self.show_actual_positions:
            self.trans_target_plots[1] = self.fixed_plot.scatter(
                self.target_point[0, 0],
                self.target_point[0, 1],
                s=36, c='black', marker='+')

class AddFiducialMarker:
    """
    A class to handle mouse press events, adding a fiducial
    marker.
    """

    def __init__(self, fig, plotter,
                 pbr, logger):
        """
        :params fig: the matplot lib figure to get mouse events from
        :params fixed_plot: the fixed image subplot
        :params moving_plot: the moving image subplot
        :params target: 1x3 target point
        :params fixed_fle: the standard deviations of the fixed image fle
        :params moving_fle: the standard deviations of the moving image fle
        """

        self.pbr = pbr
        self.plotter = plotter
        self.fig = fig
        self.cid = fig.canvas.mpl_connect('button_press_event', self)
        self.logger = logger
        self.fixed_points = None
        self.moving_points = None
        self.fids_plot = None
        self.reset_fiducials(0.0)

    def __call__(self, event):
        if event.xdata is not None:
            fiducial_location = np.zeros((1, 3), dtype=np.float64)
            fiducial_location[0, 0] = event.xdata
            fiducial_location[0, 1] = event.ydata

            if _is_valid_fiducial(fiducial_location):
                fixed_point = _add_guassian_fle_to_fiducial(
                    fiducial_location, self.pbr.fixed_fle)
                moving_point = _add_guassian_fle_to_fiducial(
                    fiducial_location, self.pbr.moving_fle)
                self.fixed_points = np.concatenate(
                    (self.fixed_points, fixed_point), axis=0)
                self.moving_points = np.concatenate(
                    (self.moving_points, moving_point), axis=0)

                [success, fre, mean_fle, expected_tre_sq,
                 expected_fre, transformed_target_2d,
                 actual_tre, no_fids] = self.pbr.register(
                     self.fixed_points, self.moving_points)

                self.plotter.plot_fiducials(self.fixed_points,
                                            self.moving_points,
                                            no_fids,
                                            mean_fle)

                if success:
                    expected_tre = math.sqrt(expected_tre_sq)
                    self.plotter.plot_registration_result(
                        actual_tre, expected_tre,
                        fre, expected_fre, transformed_target_2d)
                    self.logger.log_result(
                        actual_tre, fre, expected_tre, expected_fre, mean_fle,
                        no_fids)
                self.fig.canvas.draw()

    def reset_fiducials(self, mean_fle):
        """
        resets the fiducial markers
        """
        self.fixed_points = np.zeros((0, 3), dtype=np.float64)
        self.moving_points = np.zeros((0, 3), dtype=np.float64)
        self.plotter.plot_fiducials(self.fixed_points,
                                    self.moving_points,
                                    0, mean_fle)


def _is_valid_fiducial(_unused_fiducial_location):
    """
    Checks the x, y, and z location of a fiducial
    :returns: true if a valid fiducial
    """
    return True

def _add_guassian_fle_to_fiducial(fiducial, fle_standard_deviation):

    return np.random.normal(fiducial, fle_standard_deviation)

def make_target_point(outline, edge_buffer=0.9):
    """
    returns a target point, that should lie
    within the outline.
    """
    #let's assume the anatomy is a circle with
    #centre, and radius
    centre = np.mean(outline, 0)
    max_radius = np.min((np.max(outline, 0) - np.min(outline, 0))/2)*edge_buffer
    radius = np.random.uniform(low=0.0, high=max_radius)
    radius = np.random.uniform(low=0.0, high=max_radius)
    angle = np.random.uniform(low=0.0, high=math.pi*2.0)
    x_ord = radius * math.cos(angle) + centre[0]
    y_ord = radius * math.sin(angle) + centre[1]
    return np.array([[x_ord, y_ord, 0.0]])

class InteractiveRegistration:
    """
    an interactive window for doing live registration
    """

    def __init__(self, image_file_name):
        """
        Creates a visualisation of the projected and
        detected screen points, which you can click on
        to measure distances
        """

        self.fig, self.subplot = plt.subplots(1, 2, figsize=(18, 8))
        self.plotter = PlotRegistrations(self.subplot[1], self.subplot[0])

        log_config = {"logger" : {
            "log file name" : "fred_results.log",
            "overwrite existing" : False
            }}

        self.logger = Logger(log_config)
        self.mouse_int = None
        self.pbr = None
        self.image_file_name = image_file_name

        self.intialise_registration()

        self.cid = self.fig.canvas.mpl_connect('key_press_event',
                                               self.keypress_event)

        plt.show()

    def keypress_event(self, event):
        """
        handle a key press event
        """
        if event.key == 'r':
            self.intialise_registration()

    def intialise_registration(self):
        """
        sets up the registration
        """
        img = skimage.io.imread(self.image_file_name)
        outline, _initial_guess = find_outer_contour(img)
        target_point = make_target_point(outline)

        self.plotter.initialise_new_reg(img, target_point, outline)

        moving_fle = np.zeros((1, 3), dtype=np.float64)
        fixed_fle = np.zeros((1, 3), dtype=np.float64)
        fixed_fle[0, 0] = np.random.uniform(low=0.5, high=5.0)
        fixed_fle[0, 1] = fixed_fle[0, 0]

        if self.pbr is None:
            self.pbr = PointBasedRegistration(target_point, fixed_fle,
                                              moving_fle)
        else:
            self.pbr.reinit(target_point, fixed_fle, moving_fle)

        if self.mouse_int is None:
            self.mouse_int = AddFiducialMarker(self.fig, self.plotter,
                                               self.pbr, self.logger)

        self.mouse_int.reset_fiducials(expected_absolute_value(fixed_fle))

        self.fig.canvas.draw()

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
