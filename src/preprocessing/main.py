import os

import dotenv

from collection_processing import process_collection
from src.preprocessing.input_data_generation import truncate_csv_files

COLLECTION_NUMBER = 0  # max: 64


def main():
    collection_paths = os.listdir("../../raw_data")
    if ".keep" in collection_paths:
        collection_paths.remove(".keep")

    collection_paths = list(filter(lambda collection: "skip" not in collection, collection_paths))
    collection_path = collection_paths[COLLECTION_NUMBER]

    dotenv.load_dotenv()

    dotenv.set_key(dotenv.find_dotenv(), "BLACK_FILE", f"../../input_data/black_{COLLECTION_NUMBER}.csv")
    dotenv.set_key(dotenv.find_dotenv(), "WHITE_FILE", f"../../input_data/white_{COLLECTION_NUMBER}.csv")
    dotenv.set_key(dotenv.find_dotenv(), "DEFAULT_WRONG", str("wrong" in collection_path))

    truncate_csv_files()
    process_collection(collection_path)


if __name__ == "__main__":
    main()
