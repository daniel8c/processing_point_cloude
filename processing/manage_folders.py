import os
import shutil
from pathlib import Path
from typing import List
from processing.message import warning


class Folder:
    def __init__(self, path):
        self.path = path

    def is_dir_empty(self):
        return len(os.listdir(self.path)) == 0

    def remove_folder(self, must_be_empty: bool):
        '''
        Removes the directory at the path specified by the object, along with all its contents.

        :param bool must_be_empty: A boolean flag indicating whether the directory should only be removed if it is empty.
        '''

        if must_be_empty == True:
            if self.is_dir_empty():
                shutil.rmtree(self.path)
            else:
                warning(f'FOLDER {self.path} NIE JEST PUSTY - NIE USUNIĘTO')
        else:
            shutil.rmtree(self.path)

    @classmethod
    def search_up_folder(cls, start_folder: Path, dirname: str) -> Path:
        '''
        Searches for a folder named `dirname` starting from `start_folder` and going up the folder hierarchy
        until it is found. Returns the Path to the directory if found, else returns None.

        Parameters:
        -----------
        :param start_folder : Path
            The Path object representing the starting directory for the search.
        :param dirname : str
            The name of the directory to search for.
        '''

        while start_folder.name != f'{dirname}':
            start_folder = start_folder.parent
        return start_folder

    @classmethod
    def walk_search_files(self, start_folder: Path, filename: str) -> List[Path]:
        '''
        Searches for files and directories with a specified filename in the specified directory and its subdirectories.

        :param start_folder: The directory to search in.
        :type start_folder: Path
        :param filename: The filename to search for.
        :type filename: str

        :return: A list of paths to the files and directories that match the specified filename.
        :rtype: List[Path]
        '''

        list_files_paths = []
        for path, folders, files in os.walk(start_folder):
            for folder in folders:
                if filename in folder:
                    list_files_paths.append(Path(path).joinpath(folder))
            for file in files:
                if filename in file:
                    list_files_paths.append(Path(path).joinpath(file))
        return list_files_paths

