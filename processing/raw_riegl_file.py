import os
import shutil
from typing import Union, List
from pathlib import Path
from colorama import Fore, Style
from processing.manage_folders import Folder
from processing.message import info, warning


class RawRieglFile:
    def __init__(self, path_to_file: str):
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
            print(f'Rozmiar pliku {os.path.basename(paths)}: {file_size:.2f} MB')
        else:
            file_size = 0
            for path in paths:
                file_size += os.path.getsize(path) / den_mb
                print(f'Rozmiar pliku {os.path.basename(path)}: {os.path.getsize(path) / den_mb:.2f} MB')
        return file_size

    def remove(self):
        line_files_paths = self.search_line_files()
        size = self._size_files(line_files_paths)
        for path in line_files_paths:
            try:
                shutil.rmtree(path)
                print(f'Linia {self.get_file_name()}, o wadze {size / 1024:.2f} GB została usunięta')
            except FileNotFound as err:
                print(f'{Fore.BLUE}PLIK: {path} NIE ISTNIEJE{Style.RESET_ALL}')

    def move_up(self, in_file: str, out_file: str):
        if os.path.isfile(in_file):
            if self.check_zif_file_exist(out_file):
                shutil.move(in_file, out_file)
                folder = Folder(os.path.dirname(in_file))
                folder.remove_folder(True)
            else:
                print(
                    f'{Fore.BLUE}PLIK {self.get_file_name()}.zif NIE ZNAJDUJE SIE W FOLDERZE: {out_file} - NIE PRZENIESIONO{Style.RESET_ALL}')
        else:
            folder = Folder(os.path.dirname(in_file))
            folder.remove_folder(True)

    def get_file_name(self) -> str:
        return os.path.splitext(os.path.basename(self.path_to_file))[0]

    def check_zif_file_exist(self, zif_folder: str) -> bool:
        zif_files = [f for f in os.listdir(zif_folder) if os.path.isfile(os.path.join(zif_folder, f))]
        return self.get_file_name() + '.zif' in zif_files

    def __str__(self):
        return f'Linia: {self.get_file_name()}'


file = RawRieglFile(r"H:\PROJECT_TESTING\NOWY_SZABLON\DANE_PRZYGOTOWANE\03_RIEGL_RAW\02_RXP\LIDAR\221017_051950.rxp")
file.search_line_files()
