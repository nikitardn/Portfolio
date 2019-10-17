"""Copyright (c) 2019 AIT Lab, ETH Zurich, Xu Chen

Students and holders of copies of this code, accompanying datasets,
and documentation, are not allowed to copy, distribute or modify
any of the mentioned materials beyond the scope and duration of the
Machine Perception course projects.

That is, no partial/full copy nor modification of this code and
accompanying data should be made publicly or privately available to
current/future students or other parties.
"""

import tensorflow as tf
import numpy as np
import patoolib


def compute_MPJPE(p3d_out,p3d_gt,p3d_std):

    p3d_out_17x3 = tf.reshape(p3d_out, [-1, 17, 3])
    p3d_gt_17x3 = tf.reshape(p3d_gt, [-1, 17, 3])

    mse = ((p3d_out_17x3 - p3d_gt_17x3) * p3d_std) ** 2
    mse = tf.reduce_sum(mse, axis=2)
    mpjpe = tf.reduce_mean(tf.sqrt(mse))

    return mpjpe

def compute_MPJPE_numpy(p3d_out,p3d_gt,p3d_std):

    p3d_out_17x3 = p3d_out.reshape([-1, 17, 3])
    p3d_gt_17x3 = p3d_gt.reshape([-1, 17, 3])

    mse = ((p3d_out_17x3 - p3d_gt_17x3) * p3d_std) ** 2
    mse = np.sum(mse, axis=2)
    mpjpe = np.mean(np.sqrt(mse))
    return mpjpe


def normalize_pose(p3d,p3d_mean, p3d_std):

    root = tf.tile(tf.expand_dims(p3d[:, 0, :], axis=1), [1, 17, 1])
    p3d = p3d - root

    p3d = (p3d-p3d_mean) / p3d_std
    p3d = tf.reshape(p3d, [-1, 51])
    return p3d


def unnormalize_pose(p3d,p3d_mean, p3d_std):

    b = tf.shape(p3d)[0]

    p3d_17x3 = tf.reshape(p3d, [-1, 17, 3])
    root = p3d_17x3[:, 0, :]
    root = tf.expand_dims(root, axis=1)
    root = tf.tile(root, [1, 17, 1])
    p3d_17x3 = p3d_17x3 - root
    p3d_17x3 = p3d_17x3 * p3d_std[:b, ...] + p3d_mean[:b, ...]
    p3d = tf.reshape(p3d_17x3, [-1, 51])
    return p3d

def unnormalize_pose_numpy(p3d,p3d_mean, p3d_std):

    p3d_17x3 = p3d.reshape([-1, 17, 3])
    root = p3d_17x3[:, 0, :]
    root = np.expand_dims(root, 1)

    p3d_17x3 = p3d_17x3 - root
    p3d_17x3 = p3d_17x3 * p3d_std + p3d_mean
    p3d = p3d_17x3.reshape([-1, 51])
    return p3d

def generate_submission(predictions, out_path):
    ids = np.arange(1, predictions.shape[0] + 1).reshape([-1, 1])

    predictions = np.hstack([ids, predictions])

    joints = ['Hip', 'RHip', 'RKnee', 'RFoot', 'LHip', 'LKnee', 'LFoot', 'Spine', 'Thorax', 'Neck/Nose', 'Head',
              'LShoulder', 'LElbow', 'LWrist', 'RShoulder', 'RElbow', 'RWrist']
    header = ["Id"]

    for j in joints:
        header.append(j + "_x")
        header.append(j + "_y")
        header.append(j + "_z")

    header = ",".join(header)
    np.savetxt(out_path, predictions, delimiter=',', header=header, comments='')


submission_files =[
    "dataGenerator.py",
    "model.py",
    "test.py",
    "train.py",
    "utils.py",
    "loss.py",
    "vis.py"
]

def create_zip_code_files(output_file):
    patoolib.create_archive(output_file, submission_files)
