import pathlib, shutil
import argparse

import sqlite3

import DB_MinimalDFAs         as db1
import DB_EnumerationProgress as db2


REMOV_ENDINGS_BASE = set(('.pyc', '.toc', '.aux', '.log', '.gz', '.bbl', '.blg', '.out'))


def _clean(directory_path, removable_endings):

    for f in directory_path.iterdir():
        if f.suffix in removable_endings:
            f.unlink()
                
                
def basic(workingDir=pathlib.Path.cwd()):

    pycachePath = pathlib.Path.cwd().joinpath('__pycache__')

    if pycachePath.exists():
        shutil.rmtree(pycachePath)

    _clean(workingDir, REMOV_ENDINGS_BASE)
    
    
def __complete(workingDir=pathlib.Path.cwd(), keepResults=False, keepDB=False):

    pycachePath = pathlib.Path.cwd().joinpath('__pycache__')

    if pycachePath.exists():
        shutil.rmtree(pycachePath)


    # clean working dir

    endingsToRemove = REMOV_ENDINGS_BASE.copy()

    if not keepResults:
        endingsToRemove |= set(('.pdf','.tex'))
        
    if not keepDB:
        endingsToRemove |= set(('.db',))
        
    _clean(workingDir, endingsToRemove)
    
    
    # clean thesis and presentation directories
    
    _clean(pathlib.Path.cwd() / 'thesis',       REMOV_ENDINGS_BASE | set(('.pdf'),))
    _clean(pathlib.Path.cwd() / 'presentation', REMOV_ENDINGS_BASE | set(('.pdf'),))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=str, default=pathlib.Path.cwd())
    parser.add_argument('-r', type=bool, default=False)
    parser.add_argument('-db', type=bool, default=False)
    args = parser.parse_args()

    __complete(pathlib.Path(args.p), args.r, args.db)
