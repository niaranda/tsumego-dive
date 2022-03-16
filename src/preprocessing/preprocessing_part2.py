import os
from datetime import datetime

from src.preprocessing.data_generation.input_data_generation import generate_input_data


def run():
    directory = "../../preprocessing_data"
    generated_files = os.listdir(directory)
    student_files = list(filter(lambda file: "student" in file, generated_files))
    teacher_files = list(filter(lambda file: "teacher" in file, generated_files))

    student_paths = [directory + "/" + file for file in student_files]
    teacher_paths = [directory + "/" + file for file in teacher_files]

    input_data = generate_input_data(student_paths, teacher_paths)

    with open("../../input_data/input_data.csv", "x") as file:
        file.write(input_data.to_csv())


if __name__ == "__main__":
    start = datetime.now()
    run()
    print(datetime.now() - start)
