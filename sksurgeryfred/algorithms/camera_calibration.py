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

class InteractiveMeasure:
    """A class to handle mouse press events, outputting the
    distance to a target point.
    """
    def __init__(self, fig, point):
        self.point = point
        self.cid = fig.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        print('%s click: xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single',
               event.xdata, event.ydata))
        screen_p = np.array((1, 2))
        screen_p[0] = event.xdata
        screen_p[1] = event.ydata
        print("distance = ", np.linalg.norm(screen_p - self.point))


def plot_errors_interactive(image_file_name, projected_point):
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
    subplot[0].scatter(projected_point[0, 1], projected_point[0, 2])

    _ = InteractiveMeasure(fig, (projected_point[0, 1], projected_point[0, 2]))

    plt.show()

