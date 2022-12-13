all: pyinstaller

pyinstaller:
	pip install pyinstaller
	pyinstaller fusion_editor.py --onefile
