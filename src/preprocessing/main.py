import os

from collection_processing import process_collection

COLLECTION_NUMBER = 0  # max: 64


def main():
    collection_paths = os.listdir("../../raw_data")
    if ".keep" in collection_paths:
        collection_paths.remove(".keep")

    process_collection(collection_paths[COLLECTION_NUMBER])


if __name__ == "__main__":
    main()
