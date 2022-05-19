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
num_dense = 2


# Train 02 for longer

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

model.fit(X_train, y_train, epochs=300, validation_split=0.3, batch_size=32,
          callbacks=[TensorBoard(f"./tb_logs/correct_cnn/05"), ])

model.save_weights("models/correct_cnn05")

# accuracy: 0.3285 - topk3: 0.6048 - topk5: 0.7257 - topk10: 0.8296
# val_accuracy: 0.3190 - val_topk3: 0.6030 - val_topk5: 0.7296 - val_topk10: 0.8390
model.evaluate(X_test, y_test)  # accuracy: 0.3123 - topk3: 0.5929 - topk5: 0.7266 - topk10: 0.8407
