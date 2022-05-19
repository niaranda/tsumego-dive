import random

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

# Train best model for longer

num_dense = 3


def build_model():
    model = Sequential()

    model.add(Conv2D(16, 2, padding="valid"))
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
          callbacks=[TensorBoard(f"./tb_logs/correct_cnn/04"), ])

model.save_weights("models/correct_cnn04")

# accuracy: 0.3220 - topk3: 0.5767 - topk5: 0.6846 - topk10: 0.7873
# val_accuracy: 0.3097 - val_topk3: 0.5790 - val_topk5: 0.7046 - val_topk10: 0.8211
model.evaluate(X_test, y_test)  # accuracy: 0.3089 - topk3: 0.5798 - topk5: 0.7052 - topk10: 0.8268
