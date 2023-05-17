python setup.py bdist_nuitka
PyInstaller --onefile --paths=win_venv\Lib\site-packages --paths=dist inf2cat.py
