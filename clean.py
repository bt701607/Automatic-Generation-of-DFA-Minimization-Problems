import os
import shutil

ENDINGS_OF_REMOVABLE_FILES = (".pyc", ".tex", ".pdf", ".aux", ".log", ".gz")

_listdir = os.listdir(os.getcwd())

if "__pycache__" in _listdir:
	shutil.rmtree("__pycache__")

for _file in _listdir:
	for _ending in ENDINGS_OF_REMOVABLE_FILES:
		if _file.endswith(_ending):
			os.remove(_file)
