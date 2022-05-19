import random

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.constraints import MinMaxNorm
from tensorflow.keras.layers import Dense, BatchNormalization, Conv2D, Flatten
from tensorflow.keras.metrics import TopKCategoricalAccuracy
from tensorflow.keras.regularizers import l1_l2
from tensorflow.python.keras.layers import Activation
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
num_dense = 2


# Try training for longer

def build_model():
    model = Sequential()

    model.add(Conv2D(conv_1_filters, conv_1_kernel, padding="same"))
    model.add(Activation("relu"))

    model.add(Flatten())

    model.add(Dense(
        units=2048,
        activation='relu', kernel_constraint=MinMaxNorm(),
        kernel_regularizer=l1_l2(),
        input_shape=(19 ** 2,)))

    model.add(BatchNormalization())

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

model.fit(X_train, y_train, epochs=200, validation_split=0.3, batch_size=32,
          callbacks=[TensorBoard(f"./tb_logs/correct_cnn/02"), ])

model.save_weights("models/correct_cnn02")

# accuracy: 0.3362 - topk3: 0.6098 - topk5: 0.7310 - topk10: 0.8406
# val_accuracy: 0.3244 - val_topk3: 0.6045 - val_topk5: 0.7287 - val_topk10: 0.8444
model.evaluate(X_test, y_test)  # accuracy: 0.3209 - topk3: 0.5990 - topk5: 0.7282 - topk10: 0.8427

incorrect_moves_data = pd.read_csv("input_data/incorrect_moves_data.csv", header=None)

incorrect_moves_data = np.array(incorrect_moves_data)
X_incorrect = incorrect_moves_data[:, :(19 ** 2)].reshape(-1, 19, 19, 1).astype("float")
y_incorrect = incorrect_moves_data[:, (19 ** 2):]
del incorrect_moves_data

model.evaluate(np.vstack([X_test, X_incorrect]), np.vstack([y_test, y_incorrect]))
# accuracy: 0.2903 - topk3: 0.5826 - topk5: 0.7213 - topk10: 0.8428

model.evaluate(X_incorrect, y_incorrect)
# accuracy: 0.2835 - topk3: 0.5790 - topk5: 0.7198 - topk10: 0.8429

teacher_moves_data = pd.read_csv("input_data/teacher_moves_data.csv", header=None)
teacher_moves_data = np.array(teacher_moves_data)
X_teacher = teacher_moves_data[:, :(19 ** 2)].reshape(-1, 19, 19, 1).astype("float")
y_teacher = teacher_moves_data[:, (19 ** 2):]
del teacher_moves_data

model.evaluate(X_teacher, y_teacher)
# accuracy: 0.3222 - topk3: 0.6055 - topk5: 0.7240 - topk10: 0.8248

model.save("model/cnn_model.h5")
