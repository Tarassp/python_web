from cleaner.normalizer import *
from cleaner.file_types import *
from cleaner.logger import *
from pathlib import Path
import shutil


class FolderCleaner:
    def __init__(
        self, folderPath: str, normalizer: NormalizerInterface, logger: Logger
    ):
        path = Path(folderPath)
        if not path.exists():
            raise ValueError("The specified folder does not exist.")
        if not path.is_dir():
            raise ValueError("The specified path is not a directory.")
        self.rootPath = path
        self.normalizer = normalizer
        self.logger = logger
        self.finded_extensions = {"Knowns": set(), "Unknowns": set()}

    def clean(self):
        def investigate_path(path: Path):
            if path.is_file():
                self.__process_file(path)
            else:
                self.__process_directory(path, investigate_path)

        investigate_path(self.rootPath)
        self.logger.log(self.finded_extensions, self.rootPath)

    def __process_file(self, path):
        extension = FileExtension(path.suffix.removeprefix("."))
        category = FileCategory(extension)

        if extension.is_unknown and path.suffix != "":
            self.finded_extensions["Unknowns"].add(path.suffix.removeprefix("."))
        else:
            self.finded_extensions["Knowns"].add(extension.value)

        if category == FileCategory.ARCHIVES:
            self.unarchive(path, category)

        self.move_file(path, category)

    def __process_directory(self, path, investigate_path):
        if path.stem in FileCategory.reserved_folders:
            return
        for item in path.iterdir():
            investigate_path(item)
        if not any(path.iterdir()):
            path.rmdir()
        elif path != self.rootPath:
            self.rename_folder(path)

    def move_file(self, source, category: FileCategory):
        filename = source.name
        if not category.is_unknowns:
            filename = self.normalizer.normalize(source.stem) + source.suffix
        destination = self.get_new_path(category) / filename
        source.rename(destination)

    def unarchive(self, source, category: FileCategory):
        shutil.unpack_archive(source, self.get_new_path(category) / source.stem)

    def rename_folder(self, path: Path):
        foldername = self.normalizer.normalize(path.name)
        destination = path.parent / foldername
        path.rename(destination)

    def get_new_path(self, type: FileCategory):
        path = self.rootPath / type.folder_name
        path.mkdir(parents=True, exist_ok=True)
        return path
