import numpy as np
import pandas as pd


def prepare_correct_moves_data():
    data = pd.read_csv("../../input_data/input_data.csv", index_col=0)

    print(f"Number of rows: {data.shape[0]}")

    # Filter correct moves
    data = data[data["correct"]]

    del data["correct"]
    del data["student"]

    print(f"Number of correct rows: {data.shape[0]}")

    print("Saving file...")

    with open("../../input_data/correct_moves_data.csv", "w+") as file:
        file.write(pd.DataFrame(data).to_csv(header=False, index=False))


if __name__ == "__main__":
    prepare_correct_moves_data()
