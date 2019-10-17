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
import os
from tqdm import trange
from utils import compute_MPJPE, normalize_pose
from model import get_model
from dataGenerator import DataGenerator
from loss import integral_loss, heatmap_loss

NUM_SAMPLES = 312188

# Hyper parameters
NUM_EPOCHS = 25
BATCH_SIZE = 16
LEARNING_RATE = 0.001
LOG_ITER_FREQ = 10000  # log every X samples
VAL_FRACTION = 0.001
FLOAT_TYPE = tf.float32
LOAD = False

# Path
LOG_PATH = "./log/test1/"
DATA_PATH = "/cluster/project/infk/hilliges/lectures/mp19/project2/"

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.visible_device_list = "0"

# Metric wrapper
def mpjpe_metric(y_true, y_pred):
	return compute_MPJPE(y_pred, y_true, 1100*2)

def error_(p3d_gt, p3d_out):
	p3d_std = 1100 * 2
	p3d_out_17x3 = tf.reshape(p3d_out, [-1, 17, 3])
	p3d_gt_17x3 = tf.reshape(p3d_gt, [-1, 17, 3])

	mse_x = ((p3d_out_17x3[:, :, 0] - p3d_gt_17x3[:, :, 0]) * p3d_std) ** 2
	mse_y = ((p3d_out_17x3[:, :, 1] - p3d_gt_17x3[:, :, 1]) * p3d_std) ** 2
	mse_z = ((p3d_out_17x3[:, :, 2] - p3d_gt_17x3[:, :, 2]) * p3d_std) ** 2

	mean_mse_xy = tf.reduce_mean(tf.sqrt(mse_x + mse_y))
	mean_mse_xz = tf.reduce_mean(tf.sqrt(mse_x + mse_z))
	mean_mse_yz = tf.reduce_mean(tf.sqrt(mse_y + mse_z))

	return p3d_out_17x3[0,2,0]

tf.enable_eager_execution()
with tf.Session(config=config) as sess:

	trainGenerator = DataGenerator(DATA_PATH, batch_size=BATCH_SIZE, val_fraction=VAL_FRACTION, name="train")
	valGenerator   = DataGenerator(DATA_PATH, batch_size=BATCH_SIZE, val_fraction=VAL_FRACTION, name="val")
	# define model
	model = get_model(batch_size=BATCH_SIZE)
	if LOAD:
		latest = tf.train.latest_checkpoint("./log/test8/saved_models/retrain")
		print("loading weight from", latest)
		model.load_weights(latest)

	# optimizer
	optimizer = tf.train.AdamOptimizer(learning_rate=LEARNING_RATE)
	# saver
	saver = tf.keras.callbacks.ModelCheckpoint(filepath=LOG_PATH +"saved_models/retrain/" + "model_{epoch:02d}.ckpt",
											   period=1,
											   save_weights_only=True,
											   save_best_only=False)
	# Tensorboard
	tensorboard = tf.keras.callbacks.TensorBoard(log_dir=LOG_PATH + "logs")

	losses = {'mask': heatmap_loss, 'xyz': integral_loss}
	metrics = {'xyz': mpjpe_metric}
	model.compile(loss=losses, optimizer=optimizer, metrics=metrics, loss_weights={'mask': 10.0, 'xyz': 1.0})
	model.fit_generator(generator=trainGenerator,
						epochs=NUM_EPOCHS,
						validation_data=valGenerator,
						callbacks=[tensorboard, saver],
						workers=4,
						use_multiprocessing=False,
						max_queue_size=10,
						verbose=1,
						shuffle=False)
