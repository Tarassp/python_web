from time import perf_counter
from folder_cleaner import FolderCleaner
from logger import FileLogger
from normalizer import NameNormalizer
import sys


def main():
    try:
        folder_to_clean = sys.argv[1]
    except:
        raise Exception("Provide the correct path to the folder.")
    cleaner = FolderCleaner(folder_to_clean, NameNormalizer(), FileLogger())
    cleaner.clean()
    

if __name__ == "__main__":
    start = perf_counter()
    main()
    elapsed = perf_counter() - start
    print(f"Duratoin: {elapsed}")