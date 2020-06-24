"""Functions to support MedPhys Taught Module workshop on
calibration and tracking
"""

import math
import numpy as np

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

        self.exp_tre_text = self.plot.text(-0.90, 1.10, stats_str,
                                           transform=self.plot.transAxes,
                                           fontsize=26,
                                           verticalalignment='top',
                                           bbox=self.props)

        self.tre_text = self.plot.text(-0.05, 1.10, actual_tre_str,
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

        self.fids_text = self.plot.text(-1.65, 1.10, fids_str,
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
                 pbr, logger, fixed_fle_sd, moving_fle_sd):
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
        self.fixed_fle_sd = fixed_fle_sd
        self.moving_fle_sd = moving_fle_sd

        self.reset_fiducials(0.0)

    def __call__(self, event):
        if event.xdata is not None:
            fiducial_location = np.zeros((1, 3), dtype=np.float64)
            fiducial_location[0, 0] = event.xdata
            fiducial_location[0, 1] = event.ydata

            if _is_valid_fiducial(fiducial_location):
                fixed_point = _add_guassian_fle_to_fiducial(
                    fiducial_location, self.fixed_fle_sd)
                moving_point = _add_guassian_fle_to_fiducial(
                    fiducial_location, self.moving_fle_sd)
                self.fixed_points = np.concatenate(
                    (self.fixed_points, fixed_point), axis=0)
                self.moving_points = np.concatenate(
                    (self.moving_points, moving_point), axis=0)

                [success, fre, mean_fle_sq, expected_tre_sq,
                 expected_fre_sq, transformed_target_2d,
                 actual_tre, no_fids] = self.pbr.register(
                     self.fixed_points, self.moving_points)

                mean_fle = math.sqrt(mean_fle_sq)
                self.plotter.plot_fiducials(self.fixed_points,
                                            self.moving_points,
                                            no_fids,
                                            mean_fle)

                if success:
                    expected_tre = math.sqrt(expected_tre_sq)
                    expected_fre = math.sqrt(expected_fre_sq)
                    self.plotter.plot_registration_result(
                        actual_tre, expected_tre,
                        fre, expected_fre, transformed_target_2d)
                    self.logger.log_result(
                        actual_tre, fre, expected_tre, expected_fre, mean_fle,
                        no_fids)
                self.fig.canvas.draw()

    def reset_fiducials(self, mean_fle_sq):
        """
        resets the fiducial markers
        """
        self.fixed_points = np.zeros((0, 3), dtype=np.float64)
        self.moving_points = np.zeros((0, 3), dtype=np.float64)
        self.plotter.plot_fiducials(self.fixed_points,
                                    self.moving_points,
                                    0, math.sqrt(mean_fle_sq))


def _is_valid_fiducial(_unused_fiducial_location):
    """
    Checks the x, y, and z location of a fiducial
    :returns: true if a valid fiducial
    """
    return True

def _add_guassian_fle_to_fiducial(fiducial, fle_standard_deviation):

    moved = np.random.normal(fiducial, fle_standard_deviation)
    return moved

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
