import processing
from processing.raw_riegl_file import RawRieglFile
from processing.manage_folders import Folder

def main():
    prj = processing.Project()
    for folder in prj.raw_data.iterdir():
        if folder.is_dir():
            for scanpos in folder.iterdir():
                for line in scanpos.iterdir():
                    file_riegl = RawRieglFile(line)
                    file_riegl.move_up(prj.raw_data)
    folder = Folder(folder)
    folder.remove_folder(True)


if __name__ == '__main__':
    main()






