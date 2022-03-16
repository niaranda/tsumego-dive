import os
from typing import List

import pandas as pd
from dotenv import load_dotenv


def generate_input_data(student_paths: List[str], teacher_paths: List[str]):
    student_data: pd.DataFrame = __unite_files_data(student_paths)
    teacher_data: pd.DataFrame = __unite_files_data(teacher_paths)

    data = __join_data(student_data, teacher_data)
    del student_data, teacher_data
    print(f"Number of observations: {data.shape[0]}")

    data = __remove_duplicates(data)
    print(f"Number of unique observations: {data.shape[0]}")

    data = __cut_preprocessing_data_moves(data)
    print(f"Number of unique observations after moves cut: {data.shape[0]}")

    del data["problem_id"]
    data = pd.get_dummies(data, columns=["move"], prefix="move")
    pos_columns = [str(pos) for pos in range(19**2)]
    expected_columns = ["student", "correct", "move"] + pos_columns + ["move_" + pos for pos in pos_columns]
    data = data.reindex(expected_columns, axis=1, fill_value=0)
    del data["move"]

    data = data.groupby(["student", "correct"] + pos_columns, as_index=False).sum()

    print(f"Number of observations after one hot encoding: {data.shape[0]}")

    num_student = data["student"].sum()
    num_interest = data.shape[0]
    num_teacher = num_interest - num_student
    num_correct = data["correct"].sum()

    print(f"Student observations: {num_student}, {round(num_student/num_interest*100)}%")
    print(f"Teacher observations: {num_teacher}, {round(num_teacher/num_interest*100)}%")
    print(f"Interest observations: {data.shape[0]}")
    print(f"Correct observations: {num_correct}, {round(num_correct/num_interest*100)}%")

    return data


def __join_data(student_data: pd.DataFrame, teacher_data: pd.DataFrame) -> pd.DataFrame:
    student_data.columns = [str(pos) for pos in range(19 ** 2)] + ["move", "correct", "problem_id"]
    student_data[["correct"]] = student_data[["correct"]].astype(bool)
    student_data[["student"]] = True

    teacher_data.columns = [str(pos) for pos in range(19 ** 2)] + ["move", "problem_id"]
    teacher_data[["correct"]] = False
    teacher_data[["student"]] = False

    return pd.concat([student_data, teacher_data])


def __unite_files_data(student_paths: List[str]) -> pd.DataFrame:
    result = pd.DataFrame()
    for path in student_paths:
        result = result.append(pd.read_csv(path, header=None))
    return result


def __remove_duplicates(data: pd.DataFrame) -> pd.DataFrame:
    return data.drop_duplicates(subset=data.columns.difference(["problem_id"]))


def __cut_preprocessing_data_moves(data: pd.DataFrame) -> pd.DataFrame:
    load_dotenv(override=True)
    row_cut = int(os.environ["MOVES_ROW_CUT"])
    observations = data[data["move"] > row_cut * 19]
    problem_ids = observations["problem_id"].unique()

    return data[~data["problem_id"].isin(problem_ids)]
