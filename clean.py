import os
import shutil

ENDINGS_OF_REMOVABLE_FILES_CODE = (".pyc", ".tex", ".pdf", ".aux", ".log", ".gz")

ENDINGS_OF_REMOVABLE_FILES_THESIS = (".toc", ".pdf", ".aux", ".log", ".gz")


def clean_code_dir(exceptions=()):

	_listdir = os.listdir(os.getcwd())

	if "__pycache__" in _listdir:
		shutil.rmtree("__pycache__")

	for _file in _listdir:
		for _ending in ENDINGS_OF_REMOVABLE_FILES_CODE:
			if _ending not in exceptions and _file.endswith(_ending):
				os.remove(_file)
				

def clean_thesis_dir():

	_listdir = os.listdir(os.getcwd() + "/thesis")

	for _file in _listdir:
		for _ending in ENDINGS_OF_REMOVABLE_FILES_THESIS:
			if _file.endswith(_ending):
				os.remove("thesis/" + _file)


if __name__ == "__main__":
	clean_code_dir()
	clean_thesis_dir()
