all: pyinstaller

pyinstaller:
	pip install pyinstaller
	pyinstaller ide.py --onefile
