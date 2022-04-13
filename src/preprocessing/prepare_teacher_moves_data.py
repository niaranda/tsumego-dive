import numpy as np
import pandas as pd


def prepare_teacher_moves_data():
    data = pd.read_csv("../../input_data/input_data.csv", index_col=0)
    data = data[~data["student"]]

    # Remove unnecessary columns
    del data["student"]
    del data["correct"]

    print(f"Number of initial rows: {data.shape[0]}")

    # Group by board position
    pos_columns = [str(pos) for pos in range(19 ** 2)]
    data = data.groupby(pos_columns, as_index=False).sum()
    data = np.array(data)

    print(f"Number of rows after grouping: {data.shape[0]}")

    board_data = data[:, :(19 ** 2 - 1)]
    movement_data = data[:, (19 ** 2):]

    # Inverse colors
    board_data = board_data * 2
    board_data = np.vectorize(lambda element: 1 if element == -2 else element)(board_data)
    board_data = np.vectorize(lambda element: -1 if element == 2 else element)(board_data)

    # Recover one hot encoding
    movement_data = np.vectorize(lambda element: 1 if element > 0 else element)(movement_data)

    data = np.hstack([board_data, movement_data])

    print("Saving file...")

    with open("../../input_data/teacher_moves_data.csv", "w+") as file:
        file.write(pd.DataFrame(data).to_csv(header=False, index=False))


if __name__ == "__main__":
    prepare_teacher_moves_data()
