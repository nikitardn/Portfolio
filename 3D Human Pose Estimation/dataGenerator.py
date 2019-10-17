import tensorflow as tf
import imageio
import imgaug as ia
from matplotlib import pyplot as plt
from imgaug import augmenters as iaa
import numpy as np
import os, h5py
import math
from itertools import combinations


class DataGenerator(tf.keras.utils.Sequence):
    def __init__(self, data_root, batch_size=64, val_fraction=0, name="train"):
        phase = "valid" if name == "test" else "train"

        all_image_paths = open(os.path.join(data_root, "annot", "%s_images.txt" % phase)).readlines()
        all_image_paths = [os.path.join(data_root, "images", path[:-1]) for path in all_image_paths]
        if phase=="train":
            annotations_path = os.path.join(data_root, "annot", "%s.h5" % phase)
            annotations = h5py.File(annotations_path, 'r')

        # load mean and std
        self.p3d_mean = np.loadtxt(os.path.join(data_root, 'annot', "mean.txt")) \
            .reshape([1, 17, 3]).astype(np.float32)
        self.p3d_std = np.loadtxt(os.path.join(data_root, 'annot', "std.txt")) \
            .reshape([1, 17, 3]).astype(np.float32)

        self.max = 1000

        split_index = int(len(all_image_paths) * (1.0 - val_fraction))
        if name == "train":
            self.image_paths = all_image_paths[:split_index]
            self.annotations = annotations['pose3d'][:split_index]
        elif name == "val":
            self.image_paths = all_image_paths[split_index:]
            self.annotations = annotations['pose3d'][split_index:]
        elif name == "test":
            self.image_paths = all_image_paths
        else:
            raise ValueError("Data Generator name has to be in [train, val, test]")
        self.batchSize = batch_size
        self.name = name
        self.nbImages = len(self.image_paths)

        self.augmentor = self.createAugmentor()
        self.randomOrder = np.random.permutation(self.nbImages)

    def __len__(self):
        return int(self.nbImages / self.batchSize)

    def __getitem__(self, batch_idx):
        start = self.batchSize * batch_idx
        if self.name == "test":
            indices = np.arange(start, start + self.batchSize) #  [start:start + self.batchSize]
            inputs = self.get_images(indices)
            return inputs
        else:
            indices = self.randomOrder[start:start + self.batchSize]
            inputs = self.get_images(indices)
            targets = self.normalize_pose(self.annotations[indices, :, :])
            masks = self.create_mask(targets)
            y = {'mask': masks, 'xyz': targets}
            return inputs, y

    def on_epoch_end(self):
        self.randomOrder = np.random.permutation(self.nbImages)

    def createAugmentor(self):

        seq = iaa.Sequential([
            iaa.Affine(translate_percent=0.05,                      # translation
                       scale={"x": (0.75, 1.25), "y": (0.75, 1.25)}),   # scale x or y
            iaa.AddToHueAndSaturation((-60, 60)),                   # colors
            iaa.ContrastNormalization((0.7, 1.3)),                  # contrast
            iaa.Multiply((0.5, 1.5), per_channel=True),              # brightness
        ], random_order=True)
        return seq.augment_images

    def get_images(self, indices):
        images = [imageio.imread(self.image_paths[i]) for i in indices]
        if self.name == "train":
            images = self.augmentor(images)
            #plt.imsave('aug_ex.png',np.hstack(images))
        images = np.array(images)
        images = images / 128 - 1
        return images

    def normalize_pose(self, pose):

        root = pose[:, 0, :]
        root = np.expand_dims(root,1)
        pose = pose - root

        # fix between -0.5 and 0.5
        scale = 1100 * 2
        pose = pose / scale
        pose = pose.reshape((-1,51))
        return pose

    def create_mask(self, targets):
        nb_joints = 17

        heatmap_size_x = 78
        heatmap_size_y = 78
        heatmap_size_z = 64

        mask = np.zeros(shape=[self.batchSize, nb_joints, heatmap_size_x, heatmap_size_y, heatmap_size_z])

        targets = targets.reshape((self.batchSize, nb_joints, 3))
        RANGE = 3
        for b in range(self.batchSize):
            for j in range(nb_joints):
                x = int(np.round((targets[b, j, 0] + 0.5) * (heatmap_size_x-1)))
                y = int(np.round((targets[b, j, 1] + 0.5) * (heatmap_size_y-1)))
                z = int(np.round((targets[b, j, 2] + 0.5) * (heatmap_size_z-1)))

                # Create Gaussian 3D cube around (x,y,z)
                for epsilon_x in range(RANGE):
                    for epsilon_y in range(RANGE):
                        for epsilon_z in range(RANGE):
                            if (x + epsilon_x >= heatmap_size_x or x - epsilon_x < 0 or
                                y + epsilon_y >= heatmap_size_y or y - epsilon_y < 0 or
                                z + epsilon_z >= heatmap_size_z or z - epsilon_z < 0) :
                                continue

                            distance = np.sqrt(epsilon_x**2+epsilon_y**2+epsilon_z**2)
                            gaussian_ = np.exp(-distance**2/2)/np.sqrt(2*math.pi)
                            x1 = min(x + epsilon_x, heatmap_size_x)
                            x2 = max(x - epsilon_x, 0)
                            y1 = min(y + epsilon_y, heatmap_size_y)
                            y2 = max(y - epsilon_y, 0)
                            z1 = min(z + epsilon_z, heatmap_size_x)
                            z2 = max(z - epsilon_z, 0)

                            mask[b, j, x + epsilon_x, y + epsilon_y, z + epsilon_z] = gaussian_
                            mask[b, j, x + epsilon_x, y + epsilon_y, z - epsilon_z] = gaussian_
                            mask[b, j, x + epsilon_x, y - epsilon_y, z + epsilon_z] = gaussian_
                            mask[b, j, x + epsilon_x, y - epsilon_y, z - epsilon_z] = gaussian_
                            mask[b, j, x - epsilon_x, y + epsilon_y, z + epsilon_z] = gaussian_
                            mask[b, j, x - epsilon_x, y + epsilon_y, z - epsilon_z] = gaussian_
                            mask[b, j, x - epsilon_x, y - epsilon_y, z + epsilon_z] = gaussian_
                            mask[b, j, x - epsilon_x, y - epsilon_y, z - epsilon_z] = gaussian_

        return mask
