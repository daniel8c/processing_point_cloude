import os
import shutil
from typing import Union, List
from pathlib import Path
from processing.manage_folders import Folder
from processing.message import info, warning


class RawRieglFile:
    def __init__(self, path_to_file: Path):
        self.path_to_file = Path(path_to_file)

    def search_line_files(self) -> List[Path]:
        '''
        Searches for line files in the 'DANE_PRZYGOTOWANE' directory for the line.

        :return: A list of paths to the line files.
        :rtype: List[Path]
        '''

        name = self.get_file_name()
        prep_folder = Folder.search_up_folder(self.path_to_file, 'DANE_PRZYGOTOWANE')
        line_files_paths = Folder.walk_search_files(prep_folder, name)
        if line_files_paths:
            info(f'ZNALEZIONO {len(line_files_paths)} PLIKI DLA LINII {name}')
        else:
            warning(f'NIE ZNALEZIONO ŻADNYCH PLIKÓW DLA LINII {name}')
        return line_files_paths

    def _size_files(self, paths: Union[List[str], str]) -> float:
        '''
        Calculates the size of one or more files in megabytes (MB).

        :param paths: A path or list of paths to the files.
        :type paths: Union[List[str], str]

        :return: The size of the file or files in MB.
        :rtype: float
        '''

        den_mb = 1024 * 1024
        if isinstance(paths, str):
            file_size = os.path.getsize(paths) / den_mb
            info(f'Rozmiar pliku {os.path.basename(paths)}: {file_size:.2f} MB')
        else:
            file_size = 0
            for path in paths:
                file_size += os.path.getsize(path) / den_mb
                info(f'Rozmiar pliku {os.path.basename(path)}: {os.path.getsize(path) / den_mb:.2f} MB')
        return file_size

    def remove(self):
        '''
        Remove method removes line files from the disk.

        :raises FileNotFound: If file is not found.
        '''

        line_files_paths = self.search_line_files()
        size = self._size_files(line_files_paths)
        if line_files_paths:
            try:
                for path in line_files_paths:
                    os.remove(path)
                info(f'Linia {self.get_file_name()}, o wadze {size / 1024:.2f} GB została usunięta')
            except FileNotFoundError as err:
                warning(f'PLIK: {path} NIE ISTNIEJE')


    def move_up(self, out_file: Path):
        '''
        Move line rxp file up to the output directory if ZIF file exist
        If rxp file is not found, the method removes the parent folder if is empty of the rxp file
        If moving file complete, parent folder is removing

        :param out_file: Output file path.
        '''

        if self.path_to_file.is_file():
            if self.check_zif_file_exist(out_file):
                shutil.move(self.path_to_file, out_file)
                folder = Folder(os.path.dirname(self.path_to_file))
                folder.remove_folder(True)
            else:
                warning(f'PLIK {self.get_file_name()}.zif NIE ZNAJDUJE SIE W FOLDERZE: {out_file} - NIE PRZENIESIONO')

    def get_file_name(self) -> str:
        return os.path.splitext(os.path.basename(self.path_to_file))[0]

    def check_zif_file_exist(self, zif_folder: Path) -> bool:
        zif_files = [f.name for f in zif_folder.iterdir() if f.is_file() and f.suffix == '.zif']
        return self.get_file_name() + '.zif' in zif_files

    def __str__(self):
        return f'Linia: {self.get_file_name()}'