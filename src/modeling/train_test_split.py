import random

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def split():
    random.seed(1)

    data = pd.read_csv("input_data/correct_moves_data.csv", header=None)

    data = np.array(data)

    X = data[:, :(19 ** 2)]
    y = data[:, (19 ** 2):]

    del data

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    with(open("input_data/correct_X_train.csv", "x")) as file:
        file.write(pd.DataFrame(X_train).to_csv(header=False, index=False))

    with(open("input_data/correct_X_test.csv", "x")) as file:
        file.write(pd.DataFrame(X_test).to_csv(header=False, index=False))

    with(open("input_data/correct_y_train.csv", "x")) as file:
        file.write(pd.DataFrame(y_train).to_csv(header=False, index=False))

    with(open("input_data/correct_y_test.csv", "x")) as file:
        file.write(pd.DataFrame(y_test).to_csv(header=False, index=False))


def get_train_test_data():
    X_train = np.array(pd.read_csv("input_data/correct_X_train.csv"))
    X_test = np.array(pd.read_csv("input_data/correct_X_test.csv"))
    y_train = np.array(pd.read_csv("input_data/correct_y_train.csv"))
    y_test = np.array(pd.read_csv("input_data/correct_y_test.csv"))
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    split()
