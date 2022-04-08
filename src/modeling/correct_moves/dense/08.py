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
model = build_model(Adamax(learning_rate=0.00001))

model.compile(optimizer=Adamax(learning_rate=0.00001),
              loss='categorical_crossentropy',
              metrics=['accuracy', TopKCategoricalAccuracy(k=3, name="topk3"),
                       TopKCategoricalAccuracy(k=5, name="topk5"),
                       TopKCategoricalAccuracy(k=10, name="topk10")])

model.load_weights("models/correct_dense06_Adamax200")

model.evaluate(X_train, y_train)  # accuracy: 0.2956 - topk3: 0.5497 - topk5: 0.6777 - topk10: 0.8180
model.evaluate(X_test, y_test)  # accuracy: 0.2931 - topk3: 0.5479 - topk5: 0.6811 - topk10: 0.8243

incorrect_moves_data = pd.read_csv("input_data/incorrect_moves_data.csv", header=None)

incorrect_moves_data = np.array(incorrect_moves_data)
X_incorrect = incorrect_moves_data[:, :(19 ** 2)]
y_incorrect = incorrect_moves_data[:, (19 ** 2):]
del incorrect_moves_data

model.evaluate(np.vstack([X_test, X_incorrect]), np.vstack([y_test, y_incorrect]))
# accuracy: 0.2556 - topk3: 0.5215 - topk5: 0.6636 - topk10: 0.8100