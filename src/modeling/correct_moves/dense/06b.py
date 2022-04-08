import random

import numpy as np
import pandas as pd
import tensorflow as tf
from keras import Sequential
from keras.callbacks import TensorBoard
from keras.constraints import MinMaxNorm
from keras.layers import Dense, BatchNormalization, Dropout
from keras.metrics import TopKCategoricalAccuracy
from keras.optimizer_v2.adadelta import Adadelta
from keras.optimizer_v2.adagrad import Adagrad
from keras.optimizer_v2.adam import Adam
from keras.optimizer_v2.adamax import Adamax
from keras.optimizer_v2.ftrl import Ftrl
from keras.optimizer_v2.gradient_descent import SGD
from keras.optimizer_v2.nadam import Nadam
from keras.optimizer_v2.rmsprop import RMSprop
from keras.regularizers import l1_l2
from sklearn.model_selection import train_test_split

random.seed(1)

data = pd.read_csv("input_data/correct_moves_data.csv", header=None)

data = np.array(data)

X = data[:, :(19 ** 2)]
y = data[:, (19 ** 2):]

del data

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

gpu = tf.config.experimental.list_physical_devices('GPU')[0]
tf.config.experimental.set_memory_growth(gpu, True)


def build_model(optimizer):
    model = Sequential()

    use_batch_norm = True
    use_dropout = False

    weights_constraint = "MinMaxNorm()"
    weights_regularization = "l1_l2()"

    model.add(Dense(
        units=2048,
        activation='relu', kernel_constraint=eval(weights_constraint),
        kernel_regularizer=eval(weights_regularization),
        input_shape=(19 ** 2,)))

    if use_batch_norm:
        model.add(BatchNormalization())

    if use_dropout:
        model.add(Dropout(0.5))

    num_dense = 2
    for i in range(2, num_dense + 1):
        model.add(Dense(
            units=2048,
            activation='relu', kernel_constraint=eval(weights_constraint),
            kernel_regularizer=eval(weights_regularization), ))

    if use_batch_norm:
        model.add(BatchNormalization())

    if use_dropout:
        model.add(Dropout(0.1))

    model.add(Dense(19 ** 2, activation='softmax'))

    model.compile(optimizer=optimizer,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model


# Adamax 200 epochs
# SGD more learning rate
# Adagrad more learning rate


# Adamax 200 epochs
model = build_model(Adamax(learning_rate=0.00001))

model.fit(X_train, y_train, epochs=200, validation_split=0.3, batch_size=32,
          callbacks=[TensorBoard(f"./tb_logs/correct_dense/06/Adamax200"), ])

model.save_weights(f"models/correct_dense06_Adamax200")

# use Adamax
# loss function is close to 0 -> no more improvement -> try other loss functions
