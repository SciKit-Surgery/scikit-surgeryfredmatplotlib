"""
The main widget for the interactive registration part of scikit-surgeryFRED
"""

from random import shuffle
import matplotlib.pyplot as plt

from sksurgeryfredbe.algorithms.ablation import Ablator
from sksurgeryfredbe.logging.fred_logger import Logger
from sksurgeryfred.widgets.fred_common import FredCommon

class RegistrationGame(FredCommon):
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

        self.stats_plot.set_visibilities(True, True, False, False, False,
                                         True, True, True, True)
        self.state_string = 'Actual TRE'
        self.repeats = 20
        self.visibility_setter = VisibilitySettings(self.repeats - 4)
        self.total_score = 0
        self.stats_plot.update_last_score(0)
        self.stats_plot.update_total_score(self.total_score)

        self.plotter.show_actual_positions = False

        log_config = {"logger" : {
            "log file name" : "fred_game.log",
            "overwrite existing" : False
            }}

        self.logger = Logger(log_config)
        self.ablation = Ablator(margin=1.0)

        self.initialise_registration()

        plt.rcParams['keymap.all_axes'].remove('a')
        _ = self.fig.canvas.mpl_connect('key_press_event',
                                        self.keypress_event)

        plt.show()

    def keypress_event(self, event):
        """
        handle a key press event
        """
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
                    self.logger.log_score(self.state_string, score)
                    if self.repeats > 1:
                        if self.repeats < 18:
                            [fids_text, tre_text, exp_tre_text, exp_fre_text,
                             fre_text, score_text, total_score_text,
                             margin_text, repeats_text, self.state_string] = \
                                 self.visibility_setter.get_vis_state()
                            self.stats_plot.set_visibilities(
                                fids_text, tre_text, exp_tre_text, exp_fre_text,
                                fre_text, score_text, total_score_text,
                                margin_text, repeats_text)
                        self.repeats -= 1
                        self.stats_plot.update_repeats(self.repeats)
                        self.initialise_registration()
                    else:
                        self._game_over()
                    self.fig.canvas.draw()

    def _game_over(self):
        props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
        self.fig.text(0.2, 0.7, "Game Over",
                      fontsize=56, bbox=props)

        text_str = ("Thanks for playing.\n" +
                    "Please let me know your scores by sending the log file\n" +
                    "'fred_game.log' and any comments to s.thompson@ucl.ac.uk")
        self.fig.text(0.2, 0.4, text_str,
                      fontsize=26, bbox=props)

        self.fig.canvas.draw()

    def initialise_registration(self):
        """
        sets up the registration
        """
        target_point = super().init_reg()
        self.ablation.setup(target=target_point,
                            target_radius=10.0)

        self.stats_plot.update_margin_stats(self.ablation.margin)
        self.stats_plot.update_repeats(self.repeats)

        self.fig.canvas.draw()


class VisibilitySettings:
    """
    randomly selects from list of visilities, has five states
    FLE and no fids
    Expected FRE
    Expected TRE
    Actual FRE
    """
    def __init__(self, buffer_size):
        """
        :params buffer_size: the number of repeats you want, should be a
            product of 4
        """
        if buffer_size % 4 != 0:
            raise ValueError("Buffer size must be divisible by 4")

        each_bin = int(buffer_size / 4)

        fle_and_fids = [True, False, False, False, False,
                        True, True, True, True, 'FLE and Number of Fids']
        exp_tre = [False, False, True, False, False, True, True, True, True,
                   'Expected TRE']
        exp_fre = [False, False, False, True, False, True, True, True, True,
                   'Expected FRE']
        actual_fre = [False, False, False, False, True, True, True, True, True,
                      'Actual FRE']

        self.state_list = []

        for _ in range(each_bin):
            self.state_list.append(fle_and_fids)
            self.state_list.append(exp_tre)
            self.state_list.append(exp_fre)
            self.state_list.append(actual_fre)

    def get_vis_state(self):
        """
        returns a random visibility state
        """
        shuffle(self.state_list)
        try:
            return self.state_list.pop()
        except IndexError:
            raise IndexError("You tried to get a value from" +
                             "VisibilitySettings, but" +
                             "the buffer is emptied.") from IndexError
