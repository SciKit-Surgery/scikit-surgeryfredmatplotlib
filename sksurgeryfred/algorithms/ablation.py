#  -*- coding: utf-8 -*-

"""
Functions for point based registration using Orthogonal Procrustes.
"""

class Ablator():
    """
    handles the simulated ablation for scikit-surgery fred
    """
    def __init__(self):
        """
        Initialise ablator with some empty member variables
        """
        self.margin = None
        self.target = None
        self.est_target = None
        self.target_radius = None
        self.ready = False
        self.margin_increment = 0.1

    def setup(self, margin, target, target_radius):
        """
        Setup target etc.
        """
        self.margin = margin
        self.target = target
        self.target_radius = target_radius
        self.ready = True

    def increase_margin(self):
        """
        Make the margin bigger
        """
        if self.ready:
            self.margin += self.margin_increment
            print("margin = {0:.1f}".format(self.margin))

    def decrease_margin(self):
        """
        Make the margin smaller
        """
        if self.ready:
            self.margin -= self.margin_increment
            if self.margin <= 0.0:
                self.margin = 0.0
            print("margin = {0:.1f}".format(self.margin))

    def alate(self, estimated_target):
        """
        performs and ablation, returns a score.
        """
        if not self.ready:
            return
        print("Fire: ", estimated_target)
