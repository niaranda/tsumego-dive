import gc
import os
from datetime import datetime

import dotenv

from src.preprocessing.processing.collection_processing import process_collection
from src.preprocessing.data_generation.input_data_generation import truncate_csv_files


def main():
    # Get collection paths
    collection_paths = os.listdir("../../raw_data")
    if ".keep" in collection_paths:
        collection_paths.remove(".keep")

    # Remove skipped collections
    collection_paths = list(filter(lambda collection: "skip" not in collection, collection_paths))

    for collection_number in range(60):
        collection_path = collection_paths[collection_number]

        # Define necessary environment variables
        dotenv.load_dotenv()

        dotenv.set_key(dotenv.find_dotenv(), "PRE_STUDENT_FILE", f"../../preprocessing_data/student_{collection_number}.csv")
        dotenv.set_key(dotenv.find_dotenv(), "PRE_TEACHER_FILE", f"../../preprocessing_data/teacher_{collection_number}.csv")
        dotenv.set_key(dotenv.find_dotenv(), "DEFAULT_WRONG", str("wrong" in collection_path))

        # Truncate existing csv files
        truncate_csv_files()

        # Perform processing
        process_collection(collection_path)

        # Force garbage collection
        gc.collect()


if __name__ == "__main__":
    start = datetime.now()
    main()
    print(datetime.now() - start)
