import tensorflow as tf
from tensorflow.python.keras.layers import Softmax
from tensorflow.python.keras.losses import binary_crossentropy, mean_absolute_error

def heatmap_loss(target_mask, heatmap_3d):
    X = 2
    Y = 3
    Z = 4

    dims = heatmap_3d.shape  # batches, joints, x, y, z
    batch_size = dims[0]
    nb_joints = dims[1]

    heatmap_ = tf.reshape(heatmap_3d, [batch_size, nb_joints, -1])
    heatmap_ = Softmax(axis = 2)(heatmap_)
    target_mask = tf.reshape(target_mask, [batch_size, nb_joints, -1])

    return binary_crossentropy(target_mask, heatmap_)

def integral_loss(target_true, target_pred):
    return mean_absolute_error(target_true,target_pred)
