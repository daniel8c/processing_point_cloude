import numpy as np
from shapely import LineString

from processing.read_properties import Project


# class Trajectory(Report):
#     def __init__(self):
#
#         self.create_params()
#         self._check_num_params()
#         check_with_project_lines = True
#
#
#         geom = []
#         line_names = []
#         line_numbers = []
#
#         for num, trajectory in enumerate(self.project.trj_txt):
#             line_numbers.append(num + 1)
#             line_names.append(self.read_line_name(trajectory))
#             geom.append(self.read_coordinates(trajectory))
#
#         if check_with_project_lines:
#             self.gdf_project_lines = self._create_merged_project_lines()
#
#         self.create_shp(geom, line_name=line_names, line_num=line_numbers, **self.dict_parameters)
#
#     def _create_merged_project_lines(self):
#         files_project_lines = [os.path.join(self.project.project_lines, file) for file in
#                                os.listdir(self.project.project_lines) if file.endswith('.shp')]
#
#         # Merged files to gdf if files > 1 else gdf = file
#         if len(files_project_lines) == 1:
#             gdf_project_lines = gpd.read_file(files_project_lines[0])
#         elif len(files_project_lines) > 1:
#             merged = gpd.GeoDataFrame()
#             for file in files_project_lines:
#                 gdf = gpd.read_file(file)
#                 merged = merged.append(gdf)
#             gdf_project_lines = merged
#             dir_merged_lines = os.path.join(self.project.project_lines, r'ZLACZONE_LINIE')
#             if not os.path.exists(dir_merged_lines):
#                 os.mkdir(dir_merged_lines)
#             merged_lines = os.path.join(dir_merged_lines, 'ZLACZONE_LINIE.shp')
#             self._save_shp_and_update_pl92(merged_lines, gdf_project_lines)
#         else:
#             print(f"BRAK PLIKU SHP W {self.project.project_lines} Z LINIAMI LOTU")
#
#         return gdf_project_lines
#
#     def _check_num_params(self):
#         '''Check params 3 (E,N,Z) or 6 (R,P,H,E,N,Z)'''
#         if self.num_param == 3:
#             self.dict_parameters = {'E': self.array_parameters[:, 1],
#                                     'N': self.array_parameters[:, 2],
#                                     'Z': self.array_parameters[:, 3]}
#         elif self.num_param == 6:
#             self.dict_parameters = {'R': self.array_parameters[:, 1],
#                                     'P': self.array_parameters[:, 2],
#                                     'H': self.array_parameters[:, 3],
#                                     'E': self.array_parameters[:, 4],
#                                     'N': self.array_parameters[:, 5],
#                                     'Z': self.array_parameters[:, 6]}
#
#     def read_coordinates(self, trajectory):
#         '''Reading coordinates from trajectory txt files and convert to geometry with simplify 1m'''
#
#         table = np.loadtxt(trajectory, skiprows=1, delimiter=',', usecols=[1, 2])
#         y, x = table[:, 0], table[:, 1]
#         line = LineString(zip(x, y))
#         line = line.simplify(1)
#         return line
#
#     def read_line_name(self, trajectory):
#         return trajectory.split('\\')[-1].split('- ')[-1][:-4]
#
#     def create_shp(self, geom, **kwargs):
#         kwargs['geometry'] = geom
#
#         gdf = gpd.GeoDataFrame(kwargs, crs=f'EPSG:{self.project.sr_xy}')
#
#         self._save_shp_and_update_pl92(self.project.real_lines, gdf)
#
#     def _save_shp_and_update_pl92(self, file, gdf):
#         if self.project.crs_prj:
#             gdf.to_file(file, driver="ESRI Shapefile")
#             with open(file.replace('.shp', '.prj'), 'w') as fa:
#                 fa.writelines(self.project.crs_prj)
#         else:
#             gdf.to_file(file, driver="ESRI Shapefile")
#
#     def search_project_lines(self, tollerance, file_project_line):
#         for line_real in gdf['geometry']:
#             avg_list = []
#             for num, line_project in enumerate(self.merged['geometry']):
#                 list_distances = []
#                 for point in line_real.coords:
#                     point = Point(point)
#                     distance = line_project.distance(point)
#                     list_distances.append(distance)
#
#                 # print(i, sum(list_distances)/len(list_distances))
#                 avg_list.append((sum(list_distances) / len(list_distances), num + 1))
#             avg_list.sort()
#             print(avg_list[0])

class Trajectory:
    def __init__(self, path: str):
        self.project = Project()
        self.path = path

    def main(self):
        x, y = self.read_trajectory()
        line = self.crd2geom(x, y)

    def read_trajectory(self) -> tuple:
        '''Reading coordinates from trajectory txt file'''

        table = np.loadtxt(self.path, skiprows=1, delimiter=',', usecols=[1, 2])
        y, x = table[:, 0], table[:, 1]
        return x, y

    def crd2geom(self, x: float, y: float, tollerance: float = 1) -> LineString:
        '''Convert to geometry with simplify "toolerance"'''

        line = LineString(zip(x, y))
        line = line.simplify(tollerance)
        return line

    def __add__(self, other):
        pass

    def read_line_name_riegl(self):
        line_name_riegl = trajectory.split('\\')[-1].split('- ')[-1][:-4]
        return line_name_riegl



if __name__ == '__main__':
    Trajectory(r"H:\PROJECT_TESTING\NOWY_SZABLON\DANE_PRZYGOTOWANE\09_EXPORT\TRAJECTORY\20221128-1203_PIG_LIDAR3 - 221128_073948.txt")
