from normalizer import *
from file_types import *
from logger import *
import aioshutil
from pathlib import Path
from aiopath import AsyncPath


class FolderCleaner:
    def __init__(self, folder_path: AsyncPath, normalizer: NormalizerInterface, logger: Logger):
        path = Path(folder_path)
        if not path.exists():
            raise ValueError("The specified folder does not exist.")
        if not path.is_dir():
            raise ValueError("The specified path is not a directory.")
        self.root_path = AsyncPath(path)
        self.normalizer = normalizer
        self.logger = logger
        self.finded_extensions = {'Knowns': set(), 'Unknowns': set()}

    async def clean(self):
        async def clean_folder(apath: AsyncPath):
            async for path in apath.iterdir():
                if await path.is_dir():
                    await clean_folder(path)
                else:
                    await self.process_file(path)
        await clean_folder(self.root_path)
        await self.__remove_empty_folders()
        self.logger.log(self.finded_extensions, self.root_path)

    async def process_file(self, apath: AsyncPath):
        extension = FileExtension(apath.suffix.removeprefix("."))
        category = FileCategory(extension)

        if extension.is_unknown and apath.suffix != '':
            self.finded_extensions['Unknowns'].add(
                apath.suffix.removeprefix("."))
        else:
            self.finded_extensions['Knowns'].add(extension.value)

        await self.move_file(apath, category)

    async def exclude_reserved_top_level_folders(self, folders):
        for reserved in FileCategory.reserved_folders:
            dir = AsyncPath(self.root_path / reserved)
            try:
                folders.remove(dir)
            except:
                ...

    async def __remove_empty_folders(self):
        top_level_folders = [f async for f in self.root_path.iterdir() if await f.is_dir()]
        await self.exclude_reserved_top_level_folders(top_level_folders)
        for path in top_level_folders:
            await aioshutil.rmtree(path)

    async def move_file(self, source: AsyncPath, category: FileCategory):
        filename = source.name
        if not category.is_unknowns:
            filename = await self.normalizer.normalize(source.stem) + source.suffix
        destination = await self.get_new_path(category) / filename
        await source.rename(destination)

    async def unarchive(self, source, category: FileCategory):
        await aioshutil.unpack_archive(source, self.get_new_path(category) / source.stem)

    async def rename_folder(self, path: AsyncPath):
        foldername = await self.normalizer.normalize(path.name)
        destination = path.parent / foldername
        await path.rename(destination)

    async def get_new_path(self, type: FileCategory):
        path = self.root_path / type.folder_name
        await path.mkdir(parents=True, exist_ok=True)
        return path
