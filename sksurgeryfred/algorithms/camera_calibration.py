"""Functions to support MedPhys Taught Module workshop on
calibration and tracking
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import skimage.io

from sksurgerycore.algorithms.procrustes import orthogonal_procrustes

from sksurgeryfred.algorithms.fit_contour import find_outer_contour
from sksurgeryfred.algorithms.errors_2d import compute_tre_from_fle_2d, \
                                               compute_fre_2d, \
                                               expected_absolute_value

class AddFiducialMarker:
    """
    A class to handle mouse press events, adding a fiducial
    marker.
    """

    def __init__(self, fig, fixed_plot, moving_plot, target,
                 fixed_fle, moving_fle):
        """
        :params fig: the matplot lib figure to get mouse events from
        :params fixed_plot: the fixed image subplot
        :params moving_plot: the moving image subplot
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
        self.cid = fig.canvas.mpl_connect('button_press_event', self)
        self.fixed_points = np.zeros((0, 3), dtype=np.float64)
        self.moving_points = np.zeros((0, 3), dtype=np.float64)
        self.fixed_fle = fixed_fle
        self.moving_fle = moving_fle
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

    def __call__(self, event):
        if event.xdata is not None:
            fiducial_location = np.zeros((1, 3), dtype=np.float64)
            fiducial_location[0, 0] = event.xdata
            fiducial_location[0, 1] = event.ydata

            if _is_valid_fiducial(fiducial_location):
                fixed_point = _add_guassian_fle_to_fiducial(
                    fiducial_location, self.fixed_fle)
                moving_point = _add_guassian_fle_to_fiducial(
                    fiducial_location, self.moving_fle)
                self.fixed_points = np.concatenate(
                    (self.fixed_points, fixed_point), axis=0)
                self.moving_points = np.concatenate(
                    (self.moving_points, moving_point), axis=0)

                self.fixed_plot.scatter(self.fixed_points[:, 0],
                                        self.fixed_points[:, 1],
                                        s=36, c='g')
                self.moving_plot.scatter(self.moving_points[:, 0],
                                         self.moving_points[:, 1],
                                         s=36, c='g')

                self.fids_text.remove()
                self.fids_text = self.fixed_plot.text(
                    210, 190,
                    'Number of fids = {0:}'.format(self.fixed_points.shape[0]))
                if self.fixed_points.shape[0] > 2:
                    rotation, translation, fre = orthogonal_procrustes(
                        self.fixed_points, self.moving_points)
                    mean_fle = expected_absolute_value(self.fixed_fle)
                    mean_fle_squared = mean_fle * mean_fle
                    expected_tre = compute_tre_from_fle_2d(
                        self.moving_points[:, 0:2],
                        mean_fle_squared,
                        self.target[:, 0:2])
                    expected_fre = math.sqrt(
                        compute_fre_2d(self.moving_points[:, 0:2],
                                       mean_fle_squared))

                    transformed_target = np.matmul(rotation,
                                                   self.target.transpose()) + \
                                                                   translation
                    transformed_target_2d = [transformed_target[0][0],
                                             transformed_target[1][0]]
                    self.fixed_plot.scatter(transformed_target_2d[0],
                                            transformed_target_2d[1],
                                            s=64, c='r')
                    actual_tre = np.linalg.norm(
                        transformed_target_2d - self.target[:, 0:2])

                    self.tre_text.remove()
                    self.exp_tre_text.remove()
                    self.fre_text.remove()
                    self.exp_fre_text.remove()

                    self.tre_text = self.fixed_plot.text(
                        210, 210, 'Actual TRE = {0:.3f}'.format(actual_tre))
                    self.exp_tre_text = self.fixed_plot.text(
                        210, 230,
                        'Expected TRE = {0:.3f}'.format(
                            math.sqrt(expected_tre)))
                    self.fre_text = self.fixed_plot.text(
                        210, 250, 'FRE = {0:.3f}'.format(fre))
                    self.exp_fre_text = self.fixed_plot.text(
                        210, 270, 'Expected FRE = {0:.3f}'.format(expected_fre))

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

def plot_errors_interactive(image_file_name, target_point):
    """
    Creates a visualisation of the projected and
    detected screen points, which you can click on
    to measure distances
    """
    img = mpimg.imread(image_file_name)
    img = skimage.io.imread(image_file_name)
    outline, _initial_guess = find_outer_contour(img)


    fig, subplot = plt.subplots(1, 2, figsize=(18, 8))
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

    _ = AddFiducialMarker(fig, subplot[1], subplot[0],
                          target_point, fixed_fle, moving_fle)

    plt.show()
