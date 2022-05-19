import random

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.constraints import MinMaxNorm
from tensorflow.keras.layers import Dense, BatchNormalization, Conv2D, Flatten
from tensorflow.keras.metrics import TopKCategoricalAccuracy
from tensorflow.keras.regularizers import l1_l2
from tensorflow.python.keras.optimizer_v2.adamax import Adamax

from src.modeling.train_test_split import get_train_test_data

random.seed(1)

X_train, X_test, y_train, y_test = get_train_test_data()
X_train = X_train.reshape(-1, 19, 19, 1).astype("float")
X_test = X_test.reshape(-1, 19, 19, 1).astype("float")

gpu = tf.config.experimental.list_physical_devices('GPU')[0]
tf.config.experimental.set_memory_growth(gpu, True)


def build_model():
    model = Sequential()

    model.add(Conv2D(16, (2, 2), padding="same", activation="relu"))
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

model.fit(X_train, y_train, epochs=100, validation_split=0.3, batch_size=32,
          callbacks=[TensorBoard(f"./tb_logs/correct_cnn/00"), ])

model.save_weights("models/correct_cnn00")

# accuracy: 0.3157 - topk3: 0.5801 - topk5: 0.7043 - topk10: 0.8254
# val_accuracy: 0.3048 - val_topk3: 0.5674 - val_topk5: 0.6961 - val_topk10: 0.8189

model.evaluate(X_test, y_test)  # accuracy: 0.3005 - topk3: 0.5639 - topk5: 0.6930 - topk10: 0.8182
