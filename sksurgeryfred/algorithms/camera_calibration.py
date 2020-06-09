"""Functions to support MedPhys Taught Module workshop on
calibration and tracking
"""

import csv
import xml.dom.minidom
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import skimage.io

from sksurgerycore.algorithms.procrustes import orthogonal_procrustes

from sksurgeryfred.algorithms.fit_contour import find_outer_contour


def multiply_points_by_matrix(points_in, matrix):
    """Multiply a matrix of point vectors by
    a 4x4 matrix
    :param: An n by 4 matrix of n points, the first
            column is the point ID
    :param: A 4x4 matrix
    :return: An n by 4 matrix of n transformed points
    """
    points = points_in[:, 1:4]
    rows = points.shape[0]
    ids = np.reshape(points_in[:, 0], (rows, 1))
    ones = np.reshape(np.ones(rows), (rows, 1))
    homogenous_pts = np.transpose(np.concatenate((points, ones), axis=1))

    hom_pts_out = np.transpose(np.matmul(matrix, homogenous_pts))
    pts_out = hom_pts_out[:, 0:3]
    pts_out_with_id = np.concatenate((ids, pts_out), axis=1)
    return pts_out_with_id

class AddFiducialMarker:
    """
    A class to handle mouse press events, adding a fiducial 
    marker.
    """
    def __init__(self, fig, target, fixed_fle, moving_fle):
        self.target = target
        self.cid = fig.canvas.mpl_connect('button_press_event', self)
        self.fixed_points = np.zeros((0,3),dtype=np.float64)
        self.moving_points = np.zeros((0,3),dtype=np.float64)
        self.fixed_fle = fixed_fle
        self.moving_fle = moving_fle

    def __call__(self, event):
        if event.xdata is not None:
            print('%s click: xdata=%f, ydata=%f' %
                ('double' if event.dblclick else 'single',
                event.xdata, event.ydata))
            fiducial_location = np.zeros((1, 3), dtype=np.float64)
            fiducial_location[0,0] = event.xdata
            fiducial_location[0,1] = event.ydata

            if _is_valid_fiducial(fiducial_location):
                fixed_point = _add_guassian_fle_to_fiducial(fiducial_location, self.fixed_fle)
                moving_point = _add_guassian_fle_to_fiducial(fiducial_location, self.moving_fle)
                print(self.fixed_points.shape, fixed_point.shape)
                self.fixed_points = np.concatenate((self.fixed_points, fixed_point), axis = 0)
                self.moving_points = np.concatenate((self.moving_points, moving_point), axis = 0)

                print("distance = ", np.linalg.norm(fiducial_location - self.target))

                try:
                    rotation, translation, fre = orthogonal_procrustes (self.fixed_points, self.moving_points)
                    print(rotation)
                    print(translation)
                    print(fre)

                except ValueError:
                    pass



def _is_valid_fiducial(fiducial_location):
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
    outline, initial_guess = find_outer_contour(img)


    fig, subplot = plt.subplots(1, 2, figsize=(18, 8))
    subplot[0].imshow(img)
    subplot[1].plot(outline[:, 1], outline[:, 0], '-b', lw=3)
    subplot[1].plot(initial_guess[:, 1], initial_guess[:, 0], '-r', lw=3)
    subplot[1].set_ylim([0, img.shape[0]])
    subplot[1].set_xlim([0, img.shape[1]])
    subplot[1].axis([0, img.shape[1], img.shape[0], 0])
    subplot[1].axis('scaled')

    #this is just going to show the first point in an array.
    #Could get clever and search for nearest point on click?
    subplot[0].scatter(target_point[0, 0], target_point[0, 1], s = 64, c='r')
    
    moving_fle = np.zeros((1,3), dtype=np.float64)
    fixed_fle = np.zeros((1,3), dtype=np.float64)
    fixed_fle[0,0] = 2.0
    fixed_fle[0,1] = 2.0

    _ = AddFiducialMarker(fig, target_point, fixed_fle, moving_fle)

    plt.show()

