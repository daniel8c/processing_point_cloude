import os
import time
from processing.read_properties import Project


class Delete:

    def __init__(self, rec_to_del):
        # Tworzenie instancji projektu
        project = Project()

        self.record_to_del = rec_to_del
        path_and_ext = [[r"03_RIEGL_RAW\02_RXP\LIDAR", ".rxp"],
                        [r"03_RIEGL_RAW\02_RXP\LIDAR", ".rxp.log"],
                        [r"03_RIEGL_RAW\02_RXP\LIDAR", ".rxp.pps"],
                        [r"03_RIEGL_RAW\02_RXP\LIDAR", ".zif"],
                        [r"03_RIEGL_RAW\02_RXP\LIDAR", ".rxp.riport.json"],

                        [r"03_RIEGL_RAW\04_MON\LIDAR", "_LIDAR.continuous.rxp"],
                        [r"03_RIEGL_RAW\04_MON\LIDAR", ".rxp"],

                        [r"06_RIEGL_PROC\01_SDC\Scanner_1", ".rxh"],
                        [r"06_RIEGL_PROC\01_SDC\Scanner_1", ".sdc"],
                        [r"06_RIEGL_PROC\01_SDC\Scanner_1", ".sdc.log"],
                        [r"06_RIEGL_PROC\01_SDC\Scanner_1", ".sdc.sig"],
                        [r"06_RIEGL_PROC\01_SDC\Scanner_1", ".sodx"],
                        [r"06_RIEGL_PROC\01_SDC\Scanner_1", ".sodx.log"],

                        [r"06_RIEGL_PROC\02_SDW\LIDAR", "_LIDAR.sdw"],
                        [r"06_RIEGL_PROC\02_SDW\LIDAR", "_LIDAR.sdw.sig"],

                        [r"06_RIEGL_PROC\02_SDW\Scanner_1", ".p2d.rds"],
                        [r"06_RIEGL_PROC\02_SDW\Scanner_1", ".p2d.rds.log"],
                        [r"06_RIEGL_PROC\02_SDW\Scanner_1", ".p2d.rdx"],
                        [r"06_RIEGL_PROC\02_SDW\Scanner_1", ".p2d.rdx.log"],
                        [r"06_RIEGL_PROC\02_SDW\Scanner_1", ".p3d.rds"],
                        [r"06_RIEGL_PROC\02_SDW\Scanner_1", ".p3d.rds.log"],
                        [r"06_RIEGL_PROC\02_SDW\Scanner_1", ".p3d.rds.sig"],
                        [r"06_RIEGL_PROC\02_SDW\Scanner_1", ".p3d.rdx"],
                        [r"06_RIEGL_PROC\02_SDW\Scanner_1", ".p3d.rdx.log"],
                        [r"06_RIEGL_PROC\02_SDW\Scanner_1", ".pof"],
                        [r"06_RIEGL_PROC\02_SDW\Scanner_1", ".pof.log"],
                        [r"06_RIEGL_PROC\02_SDW\Scanner_1", ".sdp"]]

        saved_memory = 0

        for i in range(0, len(self.record_to_del)):
            for j in range(0, len(path_and_ext)):
                time.sleep(0.2)
                path = os.path.join(project.data_prepared, path_and_ext[j][0],
                                    (self.record_to_del[i] + path_and_ext[j][1]))

                file_name = self.record_to_del[i] + path_and_ext[j][1]
                if os.path.isfile(path):
                    file_size = os.path.getsize(path) / 1000000
                    saved_memory += file_size
                    print("File {:35} \t exist [deleted]\t[{:.2f}MB]".format(file_name, file_size))
                    os.remove(path)
                else:
                    print("File {:35} \t NOT exist".format(file_name))
            print('\n')

        print("Saved memory: {:.2f}GB".format(saved_memory / 1000))
        print("\n" + '*' * 50)
        print('Removing unnecessary files finished!')
        print('*' * 50)


if __name__ == '__main__':
    # linie do usuniecia
    rec_to_del = ["220913_044702",
                  "220913_045023",
                  "220913_045337",
                  "220913_045659",
                  "220913_050050",
                  "220913_050946",
                  "220913_051320",
                  "220913_051653",
                  "220913_052019"]

    Delete(rec_to_del)
