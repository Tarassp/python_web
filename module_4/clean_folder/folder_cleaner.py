from concurrent.futures import ThreadPoolExecutor
import os
from threading import Thread
from normalizer import *
from file_types import *
from logger import *
from pathlib import Path
import shutil

class FolderCleaner:
    def __init__(self, folderPath: str, normalizer: NormalizerInterface, logger: Logger):
        path = Path(folderPath)
        if not path.exists():
            raise ValueError("The specified folder does not exist.")
        if not path.is_dir():
            raise ValueError("The specified path is not a directory.")
        self.rootPath = path
        self.normalizer = normalizer
        self.logger = logger
        self.finded_extensions = {'Knowns': set(), 'Unknowns': set()}

    def clean(self):
        all_folders = self.get_all_folders(self.rootPath)
        self.exclude_reserved_top_level_folders(all_folders)
        
        max_threads = 10
        with ThreadPoolExecutor(max_threads) as ex:
            ex.map(self.__process_directory, all_folders)
            
        self.__remove_empty_folders()
        
        self.logger.log(self.finded_extensions, self.rootPath)
        
    def get_all_folders(self, path):
        def get_subdirs(path):
            subfolders = [Path(f.path) for f in os.scandir(path) if f.is_dir()]
            for path in list(subfolders):
                subfolders.extend(get_subdirs(path))
            return subfolders
        
        folders = get_subdirs(path)
        folders.insert(0, self.rootPath) # add root folder to the folders
        return folders
    
    def exclude_reserved_top_level_folders(self, folders):
        for reserved in FileCategory.reserved_folders:
            dir = Path(self.rootPath / reserved)
            try:
                folders.remove(dir)
            except:
                ...
        
    def __process_file(self, path):
        extension = FileExtension(path.suffix.removeprefix("."))
        category = FileCategory(extension)
        
        if extension.is_unknown and path.suffix != '':
            self.finded_extensions['Unknowns'].add(path.suffix.removeprefix("."))
        else:
            self.finded_extensions['Knowns'].add(extension.value)
            
        self.move_file(path, category)
            
    def __process_directory(self, path: Path):
        for item in path.iterdir():
            if item.is_file():
                self.__process_file(item)
    
    def __remove_empty_folders(self):
        top_level_folders = [Path(f.path) for f in os.scandir(self.rootPath) if f.is_dir()]
        self.exclude_reserved_top_level_folders(top_level_folders)
        for path in top_level_folders:
            shutil.rmtree(path)
        
    def move_file(self, source, category: FileCategory):
        filename = source.name
        if not category.is_unknowns:
            filename = self.normalizer.normalize(source.stem) + source.suffix
        destination = self.get_new_path(category) / filename
        source.rename(destination)
        
    def unarchive(self, source, category: FileCategory):
        shutil.unpack_archive(source, self.get_new_path(category) / source.stem )
        
    def rename_folder(self, path: Path):
        foldername = self.normalizer.normalize(path.name)
        destination = path.parent / foldername
        path.rename(destination)

    def get_new_path(self, type: FileCategory):
        path = self.rootPath / type.folder_name
        path.mkdir(parents=True, exist_ok=True)
        return path