"""Functions to support MedPhys Taught Module workshop on
calibration and tracking
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import skimage.io

from sksurgerycore.algorithms.procrustes import orthogonal_procrustes

from sksurgeryfred.algorithms.fit_contour import find_outer_contour
from sksurgeryfred.algorithms.errors_2d import compute_tre_from_fle_2d, \
                                               compute_fre_2d, \
                                               expected_absolute_value

from sksurgeryfred.logging.fred_logger import Logger

class PointBasedRegistration:
    """
    Does the registration and assoctiated measures
    """

    def __init__(self, target, fixed_fle, moving_fle):
        """
        :params target: 1x3 target point
        :params fixed_fle: the standard deviations of the fixed image fle
        :params moving_fle: the standard deviations of the moving image fle
        """
        if not np.all(moving_fle == 0.0):
            raise NotImplementedError("Currently we only support zero fle ")
        if not fixed_fle[0, 0] == fixed_fle[0, 1]:
            raise NotImplementedError("We only support isotropic fle")
        if not fixed_fle[0, 2] == 0:
            raise NotImplementedError("Currently we only 2D fle ")

        self.target = target
        self.fixed_fle = fixed_fle
        self.moving_fle = moving_fle

    def register(self, fixed_points, moving_points):
        """
        Does the registration
        """
        success = False
        fre = 0.0
        mean_fle = 0.0
        expected_tre = 0.0
        expected_fre = 0.0
        transformed_target_2d = [-1.0, -1.0]
        actual_tre = 0.0

        no_fids = fixed_points.shape[0]

        if no_fids > 2:
            rotation, translation, fre = orthogonal_procrustes(
                fixed_points, moving_points)
            mean_fle = expected_absolute_value(self.fixed_fle)
            mean_fle_squared = mean_fle * mean_fle
            expected_tre = compute_tre_from_fle_2d(
                moving_points[:, 0:2],
                mean_fle_squared,
                self.target[:, 0:2])
            expected_fre = math.sqrt(
                compute_fre_2d(moving_points[:, 0:2],
                               mean_fle_squared))

            transformed_target = np.matmul(rotation,
                                           self.target.transpose()) + \
                                           translation
            transformed_target_2d = [transformed_target[0][0],
                                     transformed_target[1][0]]
            actual_tre = np.linalg.norm(
                transformed_target_2d - self.target[:, 0:2])
            success = True

        return [success, fre, mean_fle, expected_tre, expected_fre,
                transformed_target_2d, actual_tre, no_fids]


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

        self.fids_text = self.fixed_plot.text(
            210, 190, 'Number of fids = {0:}'.format(0))
        self.tre_text = self.fixed_plot.text(
            210, 210, 'Actual TRE = {0:.3f}'.format(0))
        self.exp_tre_text = self.fixed_plot.text(
            210, 230, 'Expected TRE = {0:.3f}'.format(math.sqrt(0)))
        self.fre_text = self.fixed_plot.text(
            210, 250, 'FRE = {0:.3f}'.format(0))
        self.exp_fre_text = self.fixed_plot.text(
            210, 270, 'Expected FRE = {0:.3f}'.format(0))

    def plot_fiducials(self, fixed_points, moving_points, no_fids):
        """
        Updates plot with fiducial data
        """

        self.fixed_plot.scatter(fixed_points[:, 0],
                                fixed_points[:, 1],
                                s=36, c='g')
        self.moving_plot.scatter(moving_points[:, 0],
                                 moving_points[:, 1],
                                 s=36, c='g')

        self.fids_text.remove()
        self.fids_text = self.fixed_plot.text(
            210, 190,
            'Number of fids = {0:}'.format(no_fids))


    def plot_registration_result(self, actual_tre, expected_tre,
                                 fre, expected_fre, transformed_target_2d):
        """
        Plots the results of a registration
        """
        self.tre_text.remove()
        self.exp_tre_text.remove()
        self.fre_text.remove()
        self.exp_fre_text.remove()

        self.tre_text = self.fixed_plot.text(
            210, 210, 'Actual TRE = {0:.3f}'.format(actual_tre))
        self.exp_tre_text = self.fixed_plot.text(
            210, 230,
            'Expected TRE = {0:.3f}'.format(
                expected_tre))
        self.fre_text = self.fixed_plot.text(
            210, 250, 'FRE = {0:.3f}'.format(fre))
        self.exp_fre_text = self.fixed_plot.text(
            210, 270, 'Expected FRE = {0:.3f}'.format(expected_fre))

        self.fixed_plot.scatter(transformed_target_2d[0],
                                transformed_target_2d[1],
                                s=64, c='r')

class KeyBoardEvent:
    """
    A class to handle mouse press events, adding a fiducial
    marker.
    """

    def __init__(self, fig):
        """
        :params fig: the matplot lib figure to get mouse events from
        :params fixed_plot: the fixed image subplot
        :params moving_plot: the moving image subplot
        :params target: 1x3 target point
        :params fixed_fle: the standard deviations of the fixed image fle
        :params moving_fle: the standard deviations of the moving image fle
        """

        self.cid = fig.canvas.mpl_connect('key_press_event', self)

    def __call__(self, event):
        print("Got event, ", event.key)


class AddFiducialMarker:
    """
    A class to handle mouse press events, adding a fiducial
    marker.
    """

    def __init__(self, fig, fixed_plot, moving_plot, target,
                 fixed_fle, moving_fle, logger):
        """
        :params fig: the matplot lib figure to get mouse events from
        :params fixed_plot: the fixed image subplot
        :params moving_plot: the moving image subplot
        :params target: 1x3 target point
        :params fixed_fle: the standard deviations of the fixed image fle
        :params moving_fle: the standard deviations of the moving image fle
        """

        self.pbr = PointBasedRegistration(target, fixed_fle, moving_fle)
        self.plotter = PlotRegistrations(fixed_plot, moving_plot)
        self.cid = fig.canvas.mpl_connect('button_press_event', self)
        self.fixed_points = np.zeros((0, 3), dtype=np.float64)
        self.moving_points = np.zeros((0, 3), dtype=np.float64)
        self.logger = logger

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
                                            self.moving_points, no_fids)

                if success:
                    expected_tre = math.sqrt(expected_tre_sq)
                    self.plotter.plot_registration_result(
                        actual_tre, expected_tre,
                        fre, expected_fre, transformed_target_2d)
                    self.logger.log_result(
                        actual_tre, fre, expected_tre, expected_fre, mean_fle,
                        no_fids)
                plt.show()


def _is_valid_fiducial(_unused_fiducial_location):
    """
    Checks the x, y, and z location of a fiducial
    :returns: true if a valid fiducial
    """
    return True

def _add_guassian_fle_to_fiducial(fiducial, fle_standard_deviation):

    return np.random.normal(fiducial, fle_standard_deviation)

def make_target_point():
    """
    returns a target point
    """
    return np.array([[200.0, 180, 0.0]])

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

        fig, subplot = plt.subplots(1, 2, figsize=(18, 8))

        log_config = {"logger" : {
            "log file name" : "fred_results.log",
            "overwrite existing" : False
            }}

        logger = Logger(log_config)
        self.mouse_int = None

        self.intialise_registration(image_file_name, logger, fig, subplot)

        _ = KeyBoardEvent(fig)

        plt.show()

    def intialise_registration(self, image_file_name, logger, fig, subplot):
        """
        sets up the registration
        """
        target_point = make_target_point()
        img = skimage.io.imread(image_file_name)
        outline, _initial_guess = find_outer_contour(img)

        subplot[0].imshow(img)
        subplot[1].plot(outline[:, 1], outline[:, 0], '-b', lw=3)
        subplot[1].set_ylim([0, img.shape[0]])
        subplot[1].set_xlim([0, img.shape[1]])
        subplot[1].axis([0, img.shape[1], img.shape[0], 0])
        subplot[1].axis('scaled')

        subplot[0].scatter(target_point[0, 0], target_point[0, 1], s=64, c='r')

        moving_fle = np.zeros((1, 3), dtype=np.float64)
        fixed_fle = np.zeros((1, 3), dtype=np.float64)
        fixed_fle[0, 0] = 2.0
        fixed_fle[0, 1] = 2.0

        del self.mouse_int

        self.mouse_int = AddFiducialMarker(fig, subplot[1], subplot[0],
                                           target_point, fixed_fle, moving_fle,
                                           logger)




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
