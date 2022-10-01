from cleaner.folder_cleaner import FolderCleaner
from cleaner.logger import FileLogger
from cleaner.normalizer import *
from shared.client import Client
from shared.service import Service
import sys


class CleanerClient(Client):
    @property
    def message(self) -> str:
        return "Welcome to Folder Cleaner App!\nEnter a full path to a directory or type 'exit': "

    def factory_method(self) -> Service:
        return None

    def run(self):
        hint = self.message
        while True:
            line = input(hint)

            if line.lower() == "exit":
                break

            cleaner = FolderCleaner(line, NameNormalizer(), FileLogger())
            cleaner.clean()
            print("Done!")
