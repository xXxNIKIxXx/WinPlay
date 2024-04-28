@echo off
echo Activating virtual environment...
call .\venv\Scripts\activate

echo Installing PyInstaller...
pip install pyinstaller

echo Compiling main.py...
pyinstaller --onefile --add-data="trayicon.png;." --collect-all zeroconf --noconsole .\main.py

echo Compiling audio_stream.py...
pyinstaller --onefile --noconsole --collect-all zeroconf .\audio_stream.py

echo Build process completed.

echo Deleting .spec files...
del /S /Q *.spec

echo Deleting the build folder...
rd /s /q build

echo Cleanup completed.

pause