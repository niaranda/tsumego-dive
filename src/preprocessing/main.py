import os

from collection_processing import process_collection

collection_paths = os.listdir("../../raw_data")
if ".keep" in collection_paths:
    collection_paths.remove(".keep")

for collection_path in collection_paths:
    process_collection(collection_path)
