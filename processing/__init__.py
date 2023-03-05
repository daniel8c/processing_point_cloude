import os
import codecs
import time
import math
from pathlib import Path
from processing.manage_folders import Folder

class Project:
    def __init__(self):
        # script path
        self.script_path = Path.cwd()

        # saving start_time
        self.time_start = time.time()

        # setting project path
        # print('SETTING PROJECT PATHS\n')
        self.data_prepared = Folder.search_up_folder(self.script_path, 'DANE_PRZYGOTOWANE')

        # project path
        self.project_path = self.data_prepared.parent

        self.raw_data = self.data_prepared.joinpath(r'03_RIEGL_RAW\02_RXP\LIDAR')


        self.las_data = self.data_prepared.joinpath(r'09_EXPORT\LASER_DATA')
        self.trj_data = self.data_prepared.joinpath(r'09_EXPORT\TRAJECTORY')

        self.postprocessing = self.data_prepared.joinpath(r'11_POSTPROCESSING')

        self.terra_solid = self.postprocessing.joinpath(r'02_PROJECT_TERRASOLID')

        # data preparation
        self.boundaries = self.postprocessing.joinpath(r'03_BOUNDARIES')
        self.grids_dir = self.boundaries.joinpath(r'ARKUSZE_ROBOCZE')
        self.grid_index_dir = self.boundaries.joinpath(r'SIATKA_ARKUSZY')

        self.input_area = [shape for shape in self.boundaries.iterdir() if shape.suffix == '.shp'][0]
        self.input_area_buff30m = self.grids_dir.joinpath(r'{}_BUFF30M.shp'.format(self.input_area.name)[:-4])

        # alignment
        self.report = self.terra_solid.joinpath('report.txt')
        self.parameters = self.terra_solid.joinpath('parameters.txt')

        # data density and extent
        self.analysis = self.postprocessing.joinpath(r'10_ANALYSIS')
        self.density_project = self.analysis.joinpath(r'DENSITY')
        self.denisty_for_lines = self.density_project.joinpath('FOR_LINES')
        self.denisty_for_project = self.density_project.joinpath('FOR_PROJECT')
        self.denisty_for_grids = self.density_project.joinpath('FOR_GRIDS')
        self.result = self.analysis.joinpath(r'RESULT')
        self.extent = self.analysis.joinpath(r'EXTENT')
        self.map_analysis = self.analysis.joinpath('MAPA.mxd')

        # las point block
        self.dir_buff = self.postprocessing.joinpath(r'05_BUFF_LAS_FILES')
        self.dir_clip = self.postprocessing.joinpath(r'06_CLIP_LAS_FILES')
        self.dir_all = self.postprocessing.joinpath(r'07_ALL_LAS_FILES')
        self.buff_las_files = [las for las in self.dir_buff.iterdir() if las.suffix == '.las']
        self.clip_las_files = [las for las in self.dir_buff.iterdir() if las.suffix == '.las']
        self.all_las_files = [las for las in self.dir_all.iterdir() if las.suffix == '.las']

        # reference data
        self.reference_data = self.postprocessing.joinpath(r'11_REFERENCE_DATA')
        self.work_reference_data = self.reference_data.joinpath(r'ROBOCZY')

        # documentation and file with properties project
        self.documentation = self.postprocessing.joinpath(r'12_DOCUMENTATION')
        self.info_file = self.documentation.joinpath(r'PROJECT_INFO.txt')

        # execute basic methods
        self.read_properties()
        self.assign_properties()

        # setting necessary data paths
        self.database_poland = Path(r'\\nas1\teledetekcja\BAZA_DANYCH_POLSKA\DANE_POLSKA.gdb')
        self.work_grid = self.database_poland.joinpath('Siatka_NMT_1992\PL1992_{}_NMT'.format(self.work_grid))
        self.target_grid_cloud = self.database_poland.joinpath('Siatka_NMT_1992\PL1992_{}_NMT'.format(self.grid_cloude))
        self.target_grid_models = self.database_poland.joinpath('Siatka_NMT_1992\PL1992_{}_NMT'.format(self.grid_models))

        # paths to raw files and export from riegl files
        self.rxp_files = [rxp for rxp in self.raw_data.iterdir() if rxp.suffix == '.rxp']
        self.las_files = [las for las in self.las_data.iterdir() if las.suffix == '.las']
        self.trj_txt = [trj for trj in self.trj_data.iterdir() if trj.suffix == '.txt']
        self.real_lines = self.boundaries.joinpath(r'LINIE_LOTU\RZECZYWISTE\REAL_LINES.shp')
        self.project_lines = self.boundaries.joinpath(r'LINIE_LOTU\PROJEKTOWANE')

        # path to lasdataset file
        self.las_dataset_file = self.dir_buff.joinpath('las_dataset.lasd')

        # setting start work paths
        os.chdir(self.script_path)

    def read_properties(self):
        '''Read basic values from the \DANE_PRZYGOTOWANE\11_POSTPROCESSING\12_DOCUMENTATION\PROJECT_INFO.txt file'''
        self.properties = {}
        with codecs.open(self.info_file, encoding='utf-8') as r:
            for line in r.readlines():
                value = line.rstrip()
                value = value.split(':')
                self.properties[value[0]] = value[1].replace(' ', '')

    def assign_properties(self):
        '''Assign values read from the PROJECT_INFO.txt file to variables'''

        # project
        self.project_name = self.properties['PROJEKT']
        self.disc = self.properties['LOKALIZACJA NA DYSKU']
        self.date = self.properties['DATA NALOTU']

        # cloud
        self.sr_xy = int(self.properties['WYMAGANY UKLAD XY (EPSG)'])
        self.sr_h = self.properties['WYMAGANY UKLAD WYSOKOSCIOWY']
        self.density = int(self.properties['PROJEKTOWANA GESTOSC [pkt/m^2]'])
        self.prec_xy = float(self.properties['DOKLADNOSC POZIOMA [m]'])
        self.prec_h = float(self.properties['DOKLADNOSC PIONOWA [m]'])
        self.list_class = [int(_class) for _class in self.properties['KLASY'].split(',')]
        self.last_return = self._check_true_false(self.properties['OSTATNIE ODBICIE'])
        self.work_grid = int(self.properties['ARKUSZE ROBOCZE'])
        self.grid_cloude = int(self.properties['ARKUSZE CHMURY'])
        self.lax = self._check_true_false(self.properties['PLIKI LAX'])

        # models
        self.nmt_cell_size = self.properties['NMT [m]']
        self.grid_models = int(self.properties['ARKUSZE MODELI'])
        self.prec_nmt = float(self.properties['DOKLADNOSC KONTROLI NMT [m]'])

        self._check_overlaps()
        self._upload_crs_2180()

    def _check_overlaps(self):
        '''Check if the cloud should have 12 clas (check cut overlap)'''

        self.overlaps = False
        if '12' in self.list_class:
            self.overlaps = True

    def _check_true_false(self, properties):
        '''Change values from file 'TAK" to True and "NIE" to False'''

        if properties == 'TAK':
            value = True
        elif properties == 'NIE':
            value = False
        else:
            print('BLAD W {}'.format(properties))
        return value

    def total_lines(self, list_files):
        '''Calculate the total number of lines from las files exported from RIEGL (separate lines in las files)'''

        return len(list_files)

    def _upload_crs_2180(self):
        """Update coordinate system pl-92 - error in geodataframe definition"""

        if self.sr_xy == 2180:
            self.crs_prj = r'PROJCS["ETRS_1989_Poland_CS92",GEOGCS["GCS_ETRS_1989",DATUM["D_ETRS_1989",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",-5300000.0],PARAMETER["Central_Meridian",19.0],PARAMETER["Scale_Factor",0.9993],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'
        else:
            self.crs_prj = None

    def __str__(self):
        '''Name project and flight date'''

        return 'Nazwa projektu: {}\nData nalotu: {}'.format(self.project_name, self.date)

    def measure_time(self):
        '''Measure script runtime'''

        print('Koniec pracy narzedzia\n')
        stop_time = time.time()
        total_time = stop_time - self.time_start

        if total_time > 60:
            minuts = math.trunc(total_time / 60)
            seconds = math.trunc((total_time / 60 - minuts) * 60)
            print('Czas wykonywania: {:.0f} minut i {:.0f} sekund'.format(minuts, seconds))
        else:
            print('Czas wykonywania: {:.2f} sekund'.format(total_time))