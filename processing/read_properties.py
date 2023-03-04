# -*- coding: utf-8 -*-
import os
import codecs
import time
import math


class Project:
    def __init__(self):
        # script path
        self.script_path = os.getcwd()

        # saving start_time
        self.time_start = time.time()

        # setting project path
        print('SETTING PROJECT PATH\n')
        for i in range(4):
            os.chdir('..')

        # project path
        self.project_path = os.getcwd()

        self.data_prepared = os.path.join(self.project_path, r'DANE_PRZYGOTOWANE')

        self.raw_data = os.path.join(self.data_prepared, r'03_RIEGL_RAW\02_RXP\LIDAR')
        self.las_data = os.path.join(self.data_prepared, r'09_EXPORT\LASER_DATA')
        self.trj_data = os.path.join(self.data_prepared, r'09_EXPORT\TRAJECTORY')

        self.postprocessing = os.path.join(self.data_prepared, r'11_POSTPROCESSING')

        self.terra_solid = os.path.join(self.postprocessing, r'02_PROJECT_TERRASOLID')

        # data preparation
        self.boundaries = os.path.join(self.postprocessing, r'03_BOUNDARIES')
        self.grids_dir = os.path.join(self.boundaries, r'ARKUSZE_ROBOCZE')
        self.grid_index_dir = os.path.join(self.boundaries, r'SIATKA_ARKUSZY')
        self.input_area = [os.path.join(self.boundaries, shape) for shape in os.listdir(self.boundaries) if
                           shape.endswith('shp')][0]
        self.input_area_buff30m = os.path.join(self.grids_dir,
                                               r'{}_BUFF30M.shp'.format(os.path.basename(self.input_area)[:-4]))

        # alignment
        self.report = os.path.join(self.terra_solid, 'report.txt')
        self.parameters = os.path.join(self.terra_solid, 'parameters.txt')

        # data density and extent
        self.analysis = os.path.join(self.postprocessing, r'10_ANALYSIS')
        self.density_project = os.path.join(self.analysis, r'DENSITY')
        self.denisty_for_lines = os.path.join(self.density_project, 'FOR_LINES')
        self.denisty_for_project = os.path.join(self.density_project, 'FOR_PROJECT')
        self.denisty_for_grids = os.path.join(self.density_project, 'FOR_GRIDS')
        self.result = os.path.join(self.analysis, r'RESULT')
        self.extent = os.path.join(self.analysis, r'EXTENT')
        self.map_analysis = os.path.join(self.analysis, 'MAPA.mxd')

        # las point block
        self.dir_buff = os.path.join(self.postprocessing, r'05_BUFF_LAS_FILES')
        self.buff_las_files = [os.path.join(self.dir_buff, las) for las in os.listdir(self.dir_buff) if
                               las.endswith('.las')]
        self.dir_clip = os.path.join(self.postprocessing, r'06_CLIP_LAS_FILES')
        self.clip_las_files = [os.path.join(self.dir_clip, las) for las in os.listdir(self.dir_buff) if
                               las.endswith('.las')]
        self.dir_all = os.path.join(self.postprocessing, r'07_ALL_LAS_FILES')
        self.all_las_files = [os.path.join(self.dir_all, las) for las in os.listdir(self.dir_all) if
                              las.endswith('.las')]

        # reference data
        self.reference_data = os.path.join(self.postprocessing, r'11_REFERENCE_DATA')
        self.work_reference_data = os.path.join(self.reference_data, r'ROBOCZY')

        # documentation and file with properties project
        self.documentation = os.path.join(self.postprocessing, r'12_DOCUMENTATION')
        self.info_file = os.path.join(self.documentation, r'PROJECT_INFO.txt')

        # execute basic methods
        self.read_properties()
        self.assign_properties()

        # setting necessary data paths
        self.database_poland = r'\\nas1\teledetekcja\BAZA_DANYCH_POLSKA\DANE_POLSKA.gdb'
        self.work_grid = os.path.join(self.database_poland, 'Siatka_NMT_1992\PL1992_{}_NMT'.format(self.work_grid))
        self.target_grid_cloud = os.path.join(self.database_poland,
                                              'Siatka_NMT_1992\PL1992_{}_NMT'.format(self.grid_cloude))
        self.target_grid_models = os.path.join(self.database_poland,
                                               'Siatka_NMT_1992\PL1992_{}_NMT'.format(self.grid_models))

        # paths to raw files and export from riegl files
        self.rxp_files = [os.path.join(self.raw_data, rxp) for rxp in os.listdir(self.raw_data) if rxp.endswith('.rxp')]
        self.las_files = [os.path.join(self.las_data, las) for las in os.listdir(self.las_data) if las.endswith('.las')]
        self.trj_txt = [os.path.join(self.trj_data, trj) for trj in os.listdir(self.trj_data) if trj.endswith('.txt')]
        self.real_lines = os.path.join(self.boundaries, r'LINIE_LOTU\RZECZYWISTE\REAL_LINES.shp')
        self.project_lines = os.path.join(self.boundaries, r'LINIE_LOTU\PROJEKTOWANE')

        # path to lasdataset file
        self.las_dataset_file = os.path.join(self.dir_buff, 'las_dataset.lasd')

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


if __name__ == '__main__':
    projekt = Project()
