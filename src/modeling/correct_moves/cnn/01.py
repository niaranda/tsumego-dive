import random

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.constraints import MinMaxNorm
from tensorflow.keras.layers import Dense, BatchNormalization, Conv2D, Flatten
from tensorflow.keras.metrics import TopKCategoricalAccuracy
from tensorflow.keras.regularizers import l1_l2
from tensorflow.python.keras.layers import MaxPool2D, Activation
from tensorflow.python.keras.optimizer_v2.adamax import Adamax

from src.modeling.train_test_split import get_train_test_data

random.seed(1)

X_train, X_test, y_train, y_test = get_train_test_data()
X_train = X_train.reshape(-1, 19, 19, 1).astype("float")
X_test = X_test.reshape(-1, 19, 19, 1).astype("float")

gpu = tf.config.experimental.list_physical_devices('GPU')[0]
tf.config.experimental.set_memory_growth(gpu, True)

num_conv = 1
conv_1_filters = 16
conv_1_kernel = 2
use_max_pool = False
pool_size = 2
padding = "valid"


def build_model():
    model = Sequential()

    model.add(Conv2D(conv_1_filters, conv_1_kernel, padding=padding))

    if use_max_pool:
        model.add(MaxPool2D(pool_size=(pool_size, pool_size)))
    model.add(Activation("relu"))

    for num in range(2, num_conv + 1):
        model.add(Conv2D(eval(f"conv_{num}_filters"), eval(f"conv_{num}_kernel"),
                         padding=padding))
        if use_max_pool:
            model.add(MaxPool2D(pool_size=(pool_size, pool_size)))
        model.add(Activation("relu"))

    model.add(Flatten())

    model.add(Dense(
        units=2048,
        activation='relu', kernel_constraint=MinMaxNorm(),
        kernel_regularizer=l1_l2(),
        input_shape=(19 ** 2,)))

    model.add(BatchNormalization())

    num_dense = 2
    for i in range(2, num_dense + 1):
        model.add(Dense(
            units=2048,
            activation='relu', kernel_constraint=MinMaxNorm(),
            kernel_regularizer=l1_l2()))

        model.add(BatchNormalization())

    model.add(Dense(19 ** 2, activation='softmax'))

    model.compile(optimizer=Adamax(learning_rate=0.00001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy', TopKCategoricalAccuracy(k=3, name="topk3"),
                           TopKCategoricalAccuracy(k=5, name="topk5"),
                           TopKCategoricalAccuracy(k=10, name="topk10")])
    return model


model = build_model()

model.fit(X_train, y_train, epochs=30, validation_split=0.3, batch_size=32,
          callbacks=[TensorBoard(f"./tb_logs/correct_cnn/01/4"), ])

model.save_weights("models/correct_cnn01_4")

# 1: bigger kernel
# num_conv = 1
# conv_1_filters = 16
# conv_1_kernel = 3
# use_max_pool = False
# pool_size = 2
# padding = "same"

# accuracy: 0.1625 - topk3: 0.3552 - topk5: 0.4787 - topk10: 0.6735
# val_accuracy: 0.1584 - val_topk3: 0.3522 - val_topk5: 0.4750 - val_topk10: 0.6716
model.evaluate(X_test, y_test)  # accuracy: 0.1566 - topk3: 0.3458 - topk5: 0.4729 - topk10: 0.6712
# Less accuracy

# 2: more layers
# num_conv = 2
# conv_1_filters = 16
# conv_1_kernel = 2
# conv_2_filters = 16
# conv_2_kernel = 2
# use_max_pool = False
# pool_size = 2
# padding = "same"

# accuracy: 0.1721 - topk3: 0.3869 - topk5: 0.5272 - topk10: 0.7259
# val_accuracy: 0.1681 - val_topk3: 0.3840 - val_topk5: 0.5217 - val_topk10: 0.7262
model.evaluate(X_test, y_test)  # accuracy: 0.1725 - topk3: 0.3844 - topk5: 0.5259 - topk10: 0.7267
# Also less accuracy

# 3: max pooling
# num_conv = 1
# conv_1_filters = 16
# conv_1_kernel = 2
# use_max_pool = True
# pool_size = 2
# padding = "same"

# accuracy: 0.1004 - topk3: 0.2649 - topk5: 0.3966 - topk10: 0.6234
# val_accuracy: 0.0966 - val_topk3: 0.2671 - val_topk5: 0.3967 - val_topk10: 0.6263
model.evaluate(X_test, y_test)  # accuracy: 0.0976 - topk3: 0.2641 - topk5: 0.3947 - topk10: 0.6261
# Also less accuracy

# 3: no padding
# num_conv = 1
# conv_1_filters = 16
# conv_1_kernel = 2
# use_max_pool = False
# pool_size = 2
# padding = "valid"

# accuracy: 0.1872 - topk3: 0.3997 - topk5: 0.5270 - topk10: 0.7104
# val_accuracy: 0.1835 - val_topk3: 0.4021 - val_topk5: 0.5284 - val_topk10: 0.7103
model.evaluate(X_test, y_test)  # accuracy: 0.1871 - topk3: 0.3994 - topk5: 0.5297 - topk10: 0.7101
# Also less accuracy
