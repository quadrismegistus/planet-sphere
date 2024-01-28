import os,sys

def run():
    path_repo = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0,path_repo)

    path_web = os.path.join(path_repo,'round_earth','webapp')
    path_web_files = os.path.join(path_web,'.web')
    if not os.path.exists(path_web_files):
        cmd=f'(cd "{path_web}" && reflex init && reflex run)'
    else:
        cmd=f'(cd "{path_web}" && reflex run)'
    os.system(cmd)