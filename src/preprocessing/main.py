import gc
import os
from datetime import datetime

import dotenv

from collection_processing import process_collection
from src.preprocessing.input_data_generation import truncate_csv_files


def main():
    collection_paths = os.listdir("../../raw_data")
    if ".keep" in collection_paths:
        collection_paths.remove(".keep")

    collection_paths = list(filter(lambda collection: "skip" not in collection, collection_paths))

    for collection_number in range(60):
        collection_path = collection_paths[collection_number]

        dotenv.load_dotenv()

        dotenv.set_key(dotenv.find_dotenv(), "BLACK_FILE", f"../../input_data/black_{collection_number}.csv")
        dotenv.set_key(dotenv.find_dotenv(), "WHITE_FILE", f"../../input_data/white_{collection_number}.csv")
        dotenv.set_key(dotenv.find_dotenv(), "DEFAULT_WRONG", str("wrong" in collection_path))

        truncate_csv_files()
        process_collection(collection_path)
        gc.collect()


if __name__ == "__main__":
    start = datetime.now()
    main()
    print(datetime.now() - start)
