import tensorflow as tf
from tensorflow.python.keras.applications.resnet50 import ResNet50
from tensorflow.python.keras.layers import Conv2D, Conv2DTranspose, GlobalAveragePooling2D, Dense, Input, InputLayer, Softmax, ReLU, BatchNormalization, Activation
from tensorflow.python.keras.models import Model

class TopModel(Model):
    def __init__(self):
        super(TopModel,self).__init__()
        input_filters=2048 # output of resnet
        self.output_filters=256
        self.nbJoints=17
        self.depth_dim=64

        self.deconv1 = Conv2DTranspose(filters=self.output_filters,
                                      kernel_size=4,
                                      strides=(2,2),
                                      padding="valid")
        self.relu1 = ReLU()
        self.batchnorm1 = BatchNormalization()

        self.deconv2 = Conv2DTranspose(filters=self.output_filters,
                                       kernel_size=4,
                                       strides=(2, 2),
                                       padding="valid")
        self.relu2 = ReLU()
        self.batchnorm2 = BatchNormalization()

        self.deconv3 = Conv2DTranspose(filters=self.output_filters,
                                       kernel_size=4,
                                       strides=(2, 2),
                                       padding="valid")
        self.relu3 = ReLU()
        self.batchnorm3 = BatchNormalization()

        self.final_conv = Conv2D(filters=self.nbJoints*self.depth_dim,
                                 kernel_size=1,
                                 strides=1,
                                 padding="valid")

    def prediction_from_heatmap(self, heatmaps):
        X = 2
        Y = 3
        Z = 4
        dims = heatmaps.shape  # batches, joints, x, y, z
        batch_size = dims[0]
        nb_joints = dims[1]
        max_x = tf.cast(dims[X], dtype=tf.float32)
        max_y = tf.cast(dims[Y], dtype=tf.float32)
        max_z = tf.cast(dims[Z], dtype=tf.float32)
        # reshape into batches, joints, location
        heatmaps = tf.reshape(heatmaps, [batch_size, nb_joints, dims[X] * dims[Y] * dims[Z]])
        # apply softmax on locations
        heatmaps = Softmax(axis=2)(heatmaps)
        # reshape back to batches, joints,x,y,z
        heatmaps = tf.reshape(heatmaps, dims)
        # reduce probability on each axis
        prob_x = tf.reduce_sum(heatmaps, axis=(Y, Z))
        prob_y = tf.reduce_sum(heatmaps, axis=(X, Z))
        prob_z = tf.reduce_sum(heatmaps, axis=(X, Y))

        estimate_x = prob_x * tf.range(0, max_x)
        estimate_y = prob_y * tf.range(0, max_y)
        estimate_z = prob_z * tf.range(0, max_z)

        estimate_x = tf.reduce_sum(estimate_x, axis=2, keepdims=True)
        estimate_y = tf.reduce_sum(estimate_y, axis=2, keepdims=True)
        estimate_z = tf.reduce_sum(estimate_z, axis=2, keepdims=True)

        # normalize to -0.5;+0.5
        estimate_x = estimate_x / max_x - 0.5
        estimate_y = estimate_y / max_y - 0.5
        estimate_z = estimate_z / max_z - 0.5

        prediction = tf.concat([estimate_x, estimate_y, estimate_z], axis=2)
        # reshape into batches, joints, [x,y,z]
        prediction = tf.reshape(prediction, [batch_size, nb_joints * 3])
        return prediction

    def call(self, x):
        x = self.deconv1(x)
        x = self.relu1(x)
        x = self.batchnorm1(x)

        x = self.deconv2(x)
        x = self.relu2(x)
        x = self.batchnorm2(x)

        x = self.deconv3(x)
        x = self.relu3(x)
        x = self.batchnorm3(x)

        x = self.final_conv(x)

        # reshape to have batches, x,y,z,joints
        dims = x.shape
        x = tf.reshape(x, shape=[dims[0], dims[1], dims[2], self.depth_dim, self.nbJoints])
        # transpose to : batches,joints, x, y, z
        heatmap = tf.transpose(x, perm=[0,4,1,2,3])
        prediction = self.prediction_from_heatmap(heatmap)
        return [prediction, heatmap]


def get_model(batch_size, train=True):
    resnet = ResNet50(include_top=False, weights=None, input_tensor=None, input_shape=None, pooling=None)
    top_model= TopModel()

    input = Input(shape=[256,256,3], batch_size=batch_size)
    output = resnet(input)
    print("resnet output shape:",output.shape)
    out = top_model(output)
    prediction = out[0]
    heatmap = out[1]
    # set proper names for outputs
    prediction = Activation('linear', name="xyz")(prediction)
    heatmap= Activation('linear', name="mask")(heatmap)
    if train:
        model = tf.keras.models.Model(inputs=[input], outputs=[prediction, heatmap])
    else:
        model = tf.keras.models.Model(inputs=[input], outputs=[prediction])
    return model
