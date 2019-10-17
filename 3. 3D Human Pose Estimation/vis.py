"""Copyright (c) 2019 AIT Lab, ETH Zurich, Xu Chen

Students and holders of copies of this code, accompanying datasets,
and documentation, are not allowed to copy, distribute or modify
any of the mentioned materials beyond the scope and duration of the
Machine Perception course projects.

That is, no partial/full copy nor modification of this code and
accompanying data should be made publicly or privately available to
current/future students or other parties.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import h5py
import os
import cv2

#DATA_PATH = "/cluster/project/infk/hilliges/lectures/mp19/project2/"
#DATA_PATH = "C:/Users/nikit/Documents/data"
DATA_PATH = "/home/nikita/Development/Machine_Perception/data"


def show3Dpose(channels, ax):  # blue, orange

    vals = np.reshape(channels, (17, -1))
    I = np.array([0, 1, 2, 0, 4, 5, 0, 7, 8, 9, 8, 11, 12, 8, 14, 15])  # start points
    J = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])  # end points
    LR = np.array([1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], dtype=bool)

    # Make connection matrix
    for i in np.arange(len(I)):
        x, y, z = [np.array([vals[I[i], j], vals[J[i], j]]) for j in range(3)]
        ax.plot(x, y, z, lw=2, c='r' if LR[i] else 'b')

    RADIUS = 750  # space around the subject
    xroot, yroot, zroot = vals[0, 0], vals[0, 1], vals[0, 2]
    ax.set_xlim3d([-RADIUS+xroot, RADIUS+xroot])
    ax.set_zlim3d([-RADIUS+zroot, RADIUS+zroot])
    ax.set_ylim3d([-RADIUS+yroot, RADIUS+yroot])

    ax.view_init(elev=-90., azim=-90)

    ax.get_xaxis().set_ticklabels([])
    ax.get_yaxis().set_ticklabels([])
    ax.set_zticklabels([])
    ax.set_aspect('equal')


all_image_paths = open(os.path.join(DATA_PATH,"annot","train_images.txt")).readlines()
all_image_paths = [os.path.join(DATA_PATH, "images", path[:-1]) for path in all_image_paths]

annotations_path = os.path.join(DATA_PATH,"annot","train.h5")
annotations = h5py.File(annotations_path, 'r')

for i,path in enumerate(all_image_paths):
    fig = plt.figure()
    ax_img = fig.add_subplot(131)
    ax_p2d = fig.add_subplot(132)
    ax_p3d = fig.add_subplot(133, projection='3d')

    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    ax_img.imshow(image)

    p2d = annotations["pose2d"][i]
    image_p2d = image.copy()
    for joint_id in range( p2d.shape[0]):
        joint = ( int(p2d[joint_id,0]),int(p2d[joint_id,1]))
        image_p2d = cv2.circle(image_p2d, joint, 3, (0,255,0),-1)
    ax_p2d.imshow(image_p2d)

    p3d = annotations["pose3d"][i]
    show3Dpose(p3d, ax_p3d)
    plt.show()
