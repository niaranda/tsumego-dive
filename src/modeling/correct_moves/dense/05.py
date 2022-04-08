import random

import numpy as np
import pandas as pd
import tensorflow as tf
from keras import Sequential
from keras.callbacks import TensorBoard
from keras.constraints import unit_norm, UnitNorm, MaxNorm, MinMaxNorm, NonNeg
from keras.layers import Dense, BatchNormalization, Dropout
from keras.optimizer_v2.adam import Adam
from keras.regularizers import l1, l2, l1_l2
from keras_tuner import BayesianOptimization, HyperParameters, RandomSearch
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


def build_model():
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
            kernel_regularizer=eval(weights_regularization),))

        if use_batch_norm:
            model.add(BatchNormalization())

        if use_dropout:
            model.add(Dropout(0.1))

    model.add(Dense(19 ** 2, activation='softmax'))

    model.compile(optimizer=Adam(learning_rate=0.00001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model


model = build_model()

model.fit(X_train, y_train, epochs=200, validation_split=0.3, batch_size=64,
          callbacks=[TensorBoard("./tb_logs/correct_dense/05"), ])

model.evaluate(X_train, y_train)  # loss: 14.1071 - accuracy: 0.2910
model.evaluate(X_test, y_test)  # loss: 14.4130 - accuracy: 0.2609

model.save_weights("models/correct_dense05")

# accuracy starts decreasing after 100 epochs
# try with different optimizers
