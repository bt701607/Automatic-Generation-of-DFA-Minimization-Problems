"""
module: clean.py
author: Gregor Soennichsen


"""

import pathlib
import shutil
import argparse
import sqlite3


__REMOV_ENDINGS_BASE = set(('.pyc', '.toc', '.aux', '.log', '.gz', '.bbl', '.blg', '.out'))


def _clean(directoryPath, removableEndings):

    for f in directoryPath.iterdir():
        if f.suffix in removableEndings:
            f.unlink()
                
                
def basic(outDir=pathlib.Path.cwd()):

    pycachePath = pathlib.Path.cwd().joinpath('__pycache__')

    if pycachePath.exists():
        shutil.rmtree(pycachePath)

    _clean(outDir, __REMOV_ENDINGS_BASE)
    
    
def __complete(outDir=pathlib.Path.cwd(), keepResults=False, keepDB=False):

    pycachePath = pathlib.Path.cwd().joinpath('__pycache__')

    if pycachePath.exists():
        shutil.rmtree(pycachePath)


    # clean working dir

    endingsToRemove = __REMOV_ENDINGS_BASE.copy()

    if not keepResults:
        endingsToRemove |= set(('.pdf','.tex'))
        
    if not keepDB:
        endingsToRemove |= set(('.db',))
        
    _clean(outDir, endingsToRemove)
    
    
    # clean thesis and presentation directories
    
    _clean(pathlib.Path.cwd() / 'thesis',       __REMOV_ENDINGS_BASE | set(('.pdf'),))
    _clean(pathlib.Path.cwd() / 'presentation', __REMOV_ENDINGS_BASE | set(('.pdf'),))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-p',  type=str,  default=pathlib.Path.cwd())
    parser.add_argument('-r',  type=bool, default=False)
    parser.add_argument('-db', type=bool, default=False)
    args = parser.parse_args()

    __complete(pathlib.Path(args.p), args.r, args.db)
