import numpy as np
import pandas as pd
from keras import Sequential
from keras.layers import Dense
from keras.optimizer_v2.adam import Adam
from sklearn.model_selection import train_test_split

data = pd.read_csv("input_data/correct_moves_data.csv", header=None)

data = np.array(data)

X = data[:, :(19 ** 2)]
y = data[:, (19 ** 2):]

del data

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = Sequential([
    Dense(192, activation="relu", input_shape=(19 ** 2,)),
    Dense(161, activation="relu"),
    Dense(19 ** 2, activation="softmax")
])

model.compile(optimizer=Adam(learning_rate=0.00001), loss="categorical_crossentropy", metrics=["accuracy"])
model.fit(X_train, y_train, batch_size=32, epochs=300, verbose=1, validation_split=0.3)

# bigger learning_rate made loss explode
