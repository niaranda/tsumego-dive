import numpy as np
import pandas as pd
import tensorflow as tf
from keras import Sequential
from keras.callbacks import TensorBoard
from keras.layers import Dense, BatchNormalization, Dropout
from keras.optimizer_v2.adam import Adam
from keras_tuner import BayesianOptimization, HyperParameters
from sklearn.model_selection import train_test_split

data = pd.read_csv("input_data/correct_moves_data.csv", header=None)

data = np.array(data)

X = data[:, :(19 ** 2)]
y = data[:, (19 ** 2):]

del data

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

gpu = tf.config.experimental.list_physical_devices('GPU')[0]
tf.config.experimental.set_memory_growth(gpu, True)


def build_model(hp: HyperParameters):
    model = Sequential()

    use_batch_norm = hp.Boolean("use_batch_norm")
    use_dropout = hp.Boolean("use_dropout")

    model.add(Dense(
        units=hp.Int(f'dense_1_units', min_value=64, max_value=1024, step=64),
        activation='relu',
        input_shape=(19 ** 2,)))

    if use_batch_norm:
        model.add(BatchNormalization())

    if use_dropout:
        model.add(Dropout(hp.Choice(f"dropout_dense_1", values=[0.1, 0.3, 0.5, 0.7])))

    num_dense = hp.Int("num_dense_layers", min_value=1, max_value=5)
    for i in range(2, num_dense + 1):
        model.add(Dense(
            units=hp.Int(f'dense_{i}_units', min_value=64, max_value=1024, step=64),
            activation='relu'))

        if use_batch_norm:
            model.add(BatchNormalization())

        if use_dropout:
            model.add(Dropout(hp.Choice(f"dropout_dense_{i}", values=[0.1, 0.3, 0.5, 0.7])))

    model.add(Dense(19 ** 2, activation='softmax'))

    model.compile(optimizer=Adam(learning_rate=0.00001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model


tuner = BayesianOptimization(lambda hp: build_model(hp),
                             objective="val_accuracy",
                             max_trials=10,
                             seed=1,
                             project_name="tuner/correct_dense01")

tuner.search(X_train, y_train, epochs=50, validation_split=0.3, batch_size=64, callbacks=[TensorBoard("./tb_logs/correct_dense/01")])

tuner.get_best_hyperparameters()[0].values
tuner.get_best_models()[0].evaluate(X_train, y_train)  # loss: 3.2782 - accuracy: 0.2207
tuner.get_best_models()[0].evaluate(X_test, y_test)  # loss: 3.7311 - accuracy: 0.1537

# {'use_batch_norm': True,
#  'use_dropout': True,
#  'dense_1_units': 1024,
#  'num_dense_layers': 1,
#  'dropout_dense_1': 0.1,
#  'dense_2_units': 64,
#  'dropout_dense_2': 0.1,
#  'dense_3_units': 896,
#  'dense_4_units': 64,
#  'dense_5_units': 640}

# -> few layers, many nodes
