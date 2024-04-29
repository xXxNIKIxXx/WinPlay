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

set /p autostart="Do you want to move the Files in autostart? (YES/NO): "
if /i "%autostart%"=="YES" (
    cd ./dist
    move *.* "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
    cd ..
) else if /i "%autostart%"=="NO" (
    rem
) else (
    echo Invalid input. Please type YES or NO.
)


set /p build_delete="Do you want to remove the build files? (YES/NO): "
if /i "%build_delete%"=="YES" (
    rd /s /q dist
) else if /i "%build_delete%"=="NO" (
    rem
) else (
    echo Invalid input. Please type YES or NO.
)

echo Cleanup completed.

pause