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
from tqdm import trange
from dataGenerator import DataGenerator
from utils import unnormalize_pose_numpy, unnormalize_pose, generate_submission,create_zip_code_files
from model import get_model
import numpy as np
import os
import math

# Global Attribute
BATCH_SIZE = 1 # needs to be 1 !
DATA_PATH = "/cluster/project/infk/hilliges/lectures/mp19/project2/"
SAVE_PATH= "./submitted_weights"

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.visible_device_list = "0"
with tf.Session(config=config) as sess:

    testGenerator = DataGenerator(DATA_PATH, batch_size=BATCH_SIZE, name="test")
    model=get_model(batch_size=BATCH_SIZE, train=False)
    # Load weights into the new model
    latest = tf.train.latest_checkpoint(SAVE_PATH)
    print(latest)
    model.load_weights(latest)
    # predict 3d pose
    model.compile(optimizer='adam', loss=tf.losses.mean_squared_error)
    p3d_out = model.predict_generator(testGenerator, verbose=1)

    # compute MPJPE
    p3d_out = unnormalize_pose_numpy(p3d_out, 0, 1100*2)

    generate_submission(p3d_out,"submission.csv.gz")

    create_zip_code_files("code.zip")