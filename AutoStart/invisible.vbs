Set objShell = CreateObject("WScript.Shell")

' Define the path to the Python executable and the Python script
pythonExePath = "c:/Development/WinPlay/.venv/Scripts/python.exe"
pythonScriptPath = "c:/Development/WinPlay/WinPlay/main.py"

' Construct the full command to run the Python script
fullCommand = Chr(34) & pythonExePath & Chr(34) & " " & Chr(34) & pythonScriptPath & Chr(34)

' Execute the Python script
objShell.Run fullCommand, 0, False
