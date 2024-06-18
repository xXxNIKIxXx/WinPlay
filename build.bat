@echo off
set FILE_PATH=%~dp0

cd %FILE_PATH%

if exist "AutoStart" (
    rd /s /q AutoStart
) else (
    echo AutoStart directory does not exist.
)

mkdir AutoStart
cd AutoStart

echo Set objShell = CreateObject("WScript.Shell") > invisible.vbs
echo objShell.Run WScript.Arguments(0), 0, False >> invisible.vbs

echo wscript.exe ".\invisible.vbs" ".\start.bat" > WinPlay_start.bat

echo c:/Development/WinPlay/venv/Scripts/python.exe c:/Development/WinPlay/main.py > start.bat

echo DONE

pause