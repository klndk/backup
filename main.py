import os
import datetime
from posix import DirEntry
import shutil
import configparser

def load_config(file: str) -> dict:
    paths = {}
    config = configparser.ConfigParser()
    config.read('config.ini')

    paths['DEFAULT'] = {'src' : config.get('DEFAULT', 'src'), 'dst' : config.get('DEFAULT', 'dst')}

    for section in config.sections():
        paths[section] = {
            'src': config.get(section, 'src'),
            'dst': config.get(section, 'dst'),
        }
    return paths

def copy(file: DirEntry, src: str, dst: str):
    print(os.path.join(src,file.name))
    print("copy to")
    print("\t-> ",dst, file.name)
    if file.is_file():
        shutil.copy(
            os.path.join(src, file.name),
            os.path.join(dst, file.name),
        )
    else:
        if not os.path.exists(os.path.join(dst, file.name)):
            os.mkdir(os.path.join(dst, file.name))

        for f in os.scandir(os.path.join(src, file.name)):
            copy(
                f,
                os.path.join(src, file.name),
                os.path.join(dst, file.name),
            )

today = datetime.date.today().strftime("%Y-%m-%d")
deleteBeforeDate = (datetime.date.today() + datetime.timedelta(days=-7))

paths = load_config('config.ini')

for section, cfg in paths.items():
    print("prepare", section)
    target = cfg['dst']
    for t in os.scandir(target):
        if t.is_dir():
            d = datetime.datetime.strptime(t.name, "%Y-%m-%d").date()
            if d < deleteBeforeDate:
                print("removing " + str(d))
                shutil.rmtree(os.path.join(target, d.strftime("%Y-%m-%d")))
    path = os.path.join(target, today)
    if not os.path.exists(path):
        print("creating target folder", path)
        os.mkdir(path)

for section, cfg in paths.items():
    print("===========")
    print("backup", section)
    files = os.scandir(cfg['src'])
    for file in files:
        copy(file, cfg['src'], os.path.join(cfg['dst'], today))
