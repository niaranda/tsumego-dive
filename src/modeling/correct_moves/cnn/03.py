import random

import tensorflow as tf
from keras_tuner import HyperParameters, BayesianOptimization, RandomSearch
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


# Search from scratch


def build_model(hp: HyperParameters):
    model = Sequential()

    num_conv = hp.Int("num_conv", 1, 3)

    model.add(Conv2D(hp.Int("conv_1_filters", 8, 16, 4), hp.Int("conv_1_kernel", 2, 3),
                     padding=hp.Choice("conv_1_padding", ["valid", "same"])))

    use_max_pool = hp.Boolean("use_max_pool")
    if use_max_pool:
        model.add(MaxPool2D(pool_size=hp.Int("conv_1_pool_size", 2, 4)))
    model.add(Activation("relu"))

    for num in range(2, num_conv + 1):
        model.add(Conv2D(hp.Int(f"conv_{num}_filters", 8, 16, 4),
                         hp.Int(f"conv_{num}_kernel", 2, 3),
                         padding=hp.Choice(f"conv_{num}_padding", ["valid", "same"])))
        if use_max_pool:
            model.add(MaxPool2D(pool_size=hp.Int(f"conv_{num}_pool_size", 2, 4)))
        model.add(Activation("relu"))

    model.add(Flatten())

    model.add(Dense(
        units=2048,
        activation='relu', kernel_constraint=MinMaxNorm(),
        kernel_regularizer=l1_l2(),
        input_shape=(19 ** 2,)))

    model.add(BatchNormalization())

    num_dense = hp.Int("num_dense", 1, 3)
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


tuner = RandomSearch(lambda hp: build_model(hp),
                             objective="val_accuracy",
                             max_trials=10,
                             seed=1,
                             project_name="tuner/correct_cnn03")

tuner.search(X_train, y_train, epochs=40, validation_split=0.3, batch_size=64,
             callbacks=[TensorBoard("./tb_logs/correct_cnn/03")])

tuner.get_best_hyperparameters()[0].values

# accuracy: 0.2577 - topk3: 0.4936 - topk5: 0.6195 - topk10: 0.7645
# val_accuracy: 0.2484 - val_topk3: 0.4829 - val_topk5: 0.6106 - val_topk10: 0.7565
tuner.get_best_models()[0].evaluate(X_test, y_test)  # accuracy: 0.2503 - topk3: 0.4854 - topk5: 0.6126 - topk10: 0.7587

# {'num_conv': 1,
#  'conv_1_filters': 16,
#  'conv_1_kernel': 2,
#  'conv_1_padding': 'valid',
#  'use_max_pool': False,
#  'num_dense': 3}
