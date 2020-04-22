import os

import sqlite3

import DB_MinimalDFAs         as db1
import DB_EnumerationProgress as db2


ENDINGS_OF_REMOVABLE_FILES_THESIS = (".toc", ".pdf", ".aux", ".log", ".gz", ".bbl", ".blg", ".out")

ENDINGS_OF_REMOVABLE_FILES_CODE = ENDINGS_OF_REMOVABLE_FILES_THESIS + (".tex",)


def _clean(directory_path, removable_endings):

    _listdir = os.listdir(directory_path)

    for _file in _listdir:
        for _ending in removable_endings:
            if _file.endswith(_ending):
                os.remove(directory_path + "\\" + _file)


def clean_code_dir():

    _clean(os.getcwd(), set(ENDINGS_OF_REMOVABLE_FILES_CODE))
                
                
def clean_code_dir_keep_results():

    _clean(os.getcwd(), set(ENDINGS_OF_REMOVABLE_FILES_CODE) - set((".pdf",".tex")))

def clean_thesis_dir():

    _clean(os.getcwd() + "\\thesis", set(ENDINGS_OF_REMOVABLE_FILES_THESIS))
    
    
def clean_db():

    conn = sqlite3.connect('dfa.db')
    
    db1.clear(conn)
    db2.clear(conn)
    
    db1.ensureValidity(conn)
    db2.ensureValidity(conn)
    
    conn.close()


if __name__ == "__main__":

    clean_code_dir()
    clean_thesis_dir()
    clean_db()
