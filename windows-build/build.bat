@echo off

cd %~dp0

echo "Currently in %cd%"

if "%PYTHON%" == "" (
    echo "Set the PYTHON variable to point to the directory of the python executable."
    exit 1
)

"%PYTHON%\python.exe" -m pip install pyinstaller==3.2.1 pygame==1.9.3 opencv-python==3.2.0.6 
"%PYTHON%\python.exe" -m PyInstaller KnitEditor.spec
"Inno Setup 5\ISCC.exe" KnitEditor.iss
