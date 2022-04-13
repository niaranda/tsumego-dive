import numpy as np
import pandas as pd


def prepare_incorrect_moves_data():
    data = pd.read_csv("../../input_data/input_data.csv", index_col=0)
    data = data[data["student"]]
    data = data[~data["correct"]]

    # Remove unnecessary columns
    del data["student"]
    del data["correct"]

    print(f"Number of initial rows: {data.shape[0]}")

    # Group by board position
    pos_columns = [str(pos) for pos in range(19 ** 2)]
    data = data.groupby(pos_columns, as_index=False, sort=False).sum()

    print(f"Number of rows after grouping: {data.shape[0]}")

    # Recover one hot encoding
    data = np.array(data)
    data = np.vectorize(lambda element: 1 if element > 0 else element)(data)

    print("Saving file...")

    with open("../../input_data/incorrect_moves_data.csv", "w+") as file:
        file.write(pd.DataFrame(data).to_csv(header=False, index=False))


if __name__ == "__main__":
    prepare_incorrect_moves_data()
