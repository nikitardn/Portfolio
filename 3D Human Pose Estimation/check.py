import tensorflow as tf
from tqdm import trange
from dataGenerator import DataGenerator
from utils import unnormalize_pose_numpy, unnormalize_pose, generate_submission,create_zip_code_files, compute_MPJPE_numpy
from model import get_model
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import h5py
import os
import cv2


# Global Attribute
BATCH_SIZE = 64
EPOCH_TO_LOAD = 7
PREDICT = False
#DATA_PATH = "/cluster/project/infk/hilliges/lectures/mp19/project2/"
#DATA_PATH = "C:/Users/nikit/Documents/data"
DATA_PATH = "/home/nikita/Development/Machine_Perception/data"
SAVE_PATH= "/home/nikita/Development/Machine_Perception/saved_models"

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

Generator = DataGenerator(DATA_PATH, batch_size=BATCH_SIZE, name="train")
images = Generator.__getitem__(0)[0]
#annotations = unnormalize_pose_numpy(p3d,0,2*1100)
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.visible_device_list = "0"

with tf.Session(config=config) as sess:
    if PREDICT:
        model = get_model(batch_size=BATCH_SIZE)
        # Load weights into the new model
        latest = tf.train.latest_checkpoint(SAVE_PATH)
        print("weights: ", latest)
        model.load_weights(latest)
        p3d_out,_ = model.predict(x=images, verbose=1)
        p3d_out = unnormalize_pose_numpy(p3d_out, 0, 1100 * 2)
    else:
        p3d_out = np.zeros((BATCH_SIZE, 51))
    # print("error = ", compute_MPJPE_numpy(p3d_out,p3d,1100*2))
for i, img in enumerate(images):
    fig = plt.figure()
    ax_img = fig.add_subplot(121)
    ax_p3d = fig.add_subplot(122, projection='3d')

    img = (img+1)/2
    ax_img.imshow(img)

    # p3d = annotations[i]
    p3d = p3d_out[i]
    show3Dpose(p3d, ax_p3d)
    plt.show()

