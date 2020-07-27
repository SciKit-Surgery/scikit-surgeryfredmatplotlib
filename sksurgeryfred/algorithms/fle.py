#  -*- coding: utf-8 -*-

"""
Functions for adding fiducial localisation error
"""

import numpy as np

def add_guassian_fle_to_fiducial(fiducial, fle_standard_deviation):

        #moved = np.random.normal(fiducial, fle_standard_deviation)
    uni_error = np.random.uniform(-fle_standard_deviation,fle_standard_deviation,(1,3))
   # uni_error = np.array(uni_error,(1,3))
    print (uni_error)
    return fiducial + uni_error


