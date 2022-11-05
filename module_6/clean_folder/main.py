from time import perf_counter
from folder_cleaner import FolderCleaner
from logger import FileLogger
from normalizer import NameNormalizer
import argparse
from aiopath import AsyncPath
import asyncio

# parser = argparse.ArgumentParser(description="Sorting files")
# parser.add_argument("--source", "-s", help="Source folder", required=True)

# args = vars(parser.parse_args())
# source = args.get("source")
# base_folder = AsyncPath(source)
base_folder = AsyncPath("./clean_folder/Trash")


# To check this program:
# 1. Unarchive the Trash.zip file
# 2. Execute a command: python3 ./clean_folder/main.py -s ./clean_folder/Trash
if __name__ == "__main__":
    cleaner = FolderCleaner(base_folder, NameNormalizer(), FileLogger())
    start = perf_counter()
    asyncio.run(cleaner.clean())
    elapsed = perf_counter() - start
    print(f"Duratoin: {elapsed}")
