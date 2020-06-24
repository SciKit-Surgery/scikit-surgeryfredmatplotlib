"""Functions to support MedPhys Taught Module workshop on
calibration and tracking
"""

class PlotRegStatistics():
    """
    writes the registration statistics
    """
    def __init__(self, plot):
        """
        The plot to write on
        """
        self.plot = plot

        self.texts = {
            'fids_text' : None,
            'tre_text' : None,
            'exp_tre_text' : None,
            'fre_text' : None,
            'score_text' : None,
            'total_score_text' : None,
            'margin_text' : None
            }

        self.props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)

    def update_stats_plot(self, tre, exp_tre, fre, exp_fre):
        """
        Updates the statistics display
        """
        if self.texts.get('tre_text') is not None:
            self.texts.get('tre_text').remove()
        if self.texts.get('exp_tre_text') is not None:
            self.texts.get('exp_tre_text').remove()
        if self.texts.get('fre_text') is not None:
            self.texts.get('fre_text').remove()

        stats_str = ('Expected FRE = {0:.2f}\n'.format(exp_fre) +
                     'Expected TRE = {0:.2f}'.format(exp_tre))

        actual_tre_str = ('Actual TRE = {0:.2f}'.format(tre))
        actual_fre_str = ('Actual FRE = {0:.2f}'.format(fre))

        self.texts['exp_tre_text'] = self.plot.text(
            -0.90, 1.10, stats_str, transform=self.plot.transAxes,
            fontsize=26, verticalalignment='top', bbox=self.props)

        self.texts['tre_text'] = self.plot.text(
            -0.05, 1.10, actual_tre_str, transform=self.plot.transAxes,
            fontsize=26, verticalalignment='top', bbox=self.props)

        self.texts['fre_text'] = self.plot.text(
            0.65, 1.10, actual_fre_str, transform=self.plot.transAxes,
            fontsize=26, verticalalignment='top', bbox=self.props)


    def update_fids_stats(self, no_fids, mean_fle):
        """
        Updates the fids stats display
        """
        if self.texts.get('fids_text') is not None:
            self.texts.get('fids_text').remove()

        fids_str = ('Number of fids = {0:}\n'.format(no_fids) +
                    'Expected FLE = {0:.2f}'.format(mean_fle))

        self.texts['fids_text'] = self.plot.text(
            -1.65, 1.10, fids_str, transform=self.plot.transAxes,
            fontsize=26, verticalalignment='top', bbox=self.props)


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
