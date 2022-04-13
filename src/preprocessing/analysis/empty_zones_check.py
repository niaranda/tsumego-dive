import os
from typing import List

import numpy as np
import pandas as pd
import seaborn
from dotenv import load_dotenv
from matplotlib import pyplot as plt


def check_empty_zones():
    directory = "../../../preprocessing_data"
    generated_files = os.listdir(directory)
    student_files = list(filter(lambda file: "student" in file, generated_files))
    student_paths = [directory + "/" + file for file in student_files]

    teacher_files = list(filter(lambda file: "teacher" in file, generated_files))
    teacher_paths = [directory + "/" + file for file in teacher_files]

    student_data: pd.DataFrame = __unite_files_data(student_paths)
    teacher_data: pd.DataFrame = __unite_files_data(teacher_paths)

    student_data.columns = [str(pos) for pos in range(19 ** 2)] + ["move", "correct", "problem_id"]
    teacher_data.columns = [str(pos) for pos in range(19 ** 2)] + ["move", "problem_id"]

    student_data[["correct"]] = student_data[["correct"]].astype(bool)
    teacher_data[["correct"]] = False

    student_data[["student"]] = True
    teacher_data[["student"]] = False

    data = pd.concat([student_data, teacher_data])
    print(data.shape[0])
    data = __remove_duplicates(data)
    print(data.shape[0])

    moves_count = data["move"].value_counts().sort_index()
    moves_count = np.array(moves_count).reshape(19, 19)
    seaborn.heatmap(moves_count, annot=True, fmt="d")

    seaborn.heatmap(moves_count > 100, annot=True, fmt="d")
    plt.show()

    total = data.shape[0]
    seaborn.heatmap(moves_count/total*100, annot=True, fmt=".1f")

    load_dotenv(override=True)
    row_cut = int(os.environ["MOVES_ROW_CUT"])
    observations = data[data["move"] > row_cut * 19]
    problem_ids = observations["problem_id"].unique()

    cut_data = data[~data["problem_id"].isin(problem_ids)]
    print(cut_data.shape[0])
    cut_moves_count = cut_data["move"].value_counts().sort_index()

    cut_moves_count = cut_moves_count.reindex(range(row_cut * 19), fill_value=0)
    cut_moves_count = np.array(cut_moves_count).reshape(row_cut, 19)
    seaborn.heatmap(cut_moves_count, annot=True, fmt="d")

    board_data = cut_data.iloc[:, :(19 ** 2)]
    board_data_count = np.array((board_data > 0).sum()).reshape(19, 19)
    seaborn.heatmap(board_data_count, annot=True, fmt="d")

    cut_point = cut_data.shape[0] * 0.005
    seaborn.heatmap(board_data_count > cut_point)

    cut_point = cut_data.shape[0] * 0.01
    seaborn.heatmap(board_data_count > cut_point)


def __unite_files_data(student_paths: List[str]) -> pd.DataFrame:
    result = pd.DataFrame()
    for path in student_paths:
        result = result.append(pd.read_csv(path, header=None))
    return result


def __remove_duplicates(data: pd.DataFrame) -> pd.DataFrame:
    return data.drop_duplicates(subset=data.columns.difference(["problem_id"]))


if __name__ == "__main__":
    check_empty_zones()
