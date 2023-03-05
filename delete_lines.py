from processing import Project
from processing.raw_riegl_file import RawRieglFile
from typing import List

def main(list_to_delete: List[str]):
    prj = Project()
    for line in list_to_delete:
        for file in prj.raw_data.iterdir():
            if file.name == line + '.rxp':
                riegl_file = RawRieglFile(file)
                riegl_file.remove()
    else:
        print(f'LINIA {line} NIE ISTNIEJE')

if __name__ == '__main__':
    list_to_delete = ['221017_051950']
    main(list_to_delete)
