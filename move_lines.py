import os

import processing
from processing.raw_riegl_file import RawRieglFile

def main():
    prj = processing.Project()
    folders_list = [os.path.join(prj.raw_data, folder) for folder in os.listdir(prj.raw_data)]
    for folder in folders_list:
        if os.path.isdir(folder):
            scanpos_list = [os.path.join(folder, scanpos) for scanpos in os.listdir(folder)]
            for scanpos in scanpos_list:
                lines_in_scanpos = [os.path.join(scanpos, file) for file in os.listdir(scanpos)]
                for line in lines_in_scanpos:
                    file_riegl = RawRieglFile(line)
                    file_riegl.move_up(line, prj.raw_data)


if __name__ == '__main__':
    main()






