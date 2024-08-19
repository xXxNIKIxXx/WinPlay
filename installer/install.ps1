if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    $newProc = Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File', $PSCommandPath -Verb RunAs
    exit
}


New-Item temp -ItemType Directory
Set-Location .\\temp
Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.5/python-3.12.5-embed-amd64.zip -OutFile python-3.12.5-embed-amd64.zip
Expand-Archive .\\python-3.12.5-embed-amd64.zip
Set-Location .\\python-3.12.5-embed-amd64
Add-Content -Path .\python312._pth -Value 'import site'
Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py
& .\python.exe get-pip.py
Remove-Item get-pip.py
Set-Location ..
Start-Sleep -Seconds 1
Rename-Item .\python-3.12.5-embed-amd64\ .venv

Invoke-WebRequest -Uri https://github.com/xXxNIKIxXx/WinPlay/archive/refs/heads/main.zip -OutFile WinPlay.zip
Expand-Archive .\\WinPlay.zip
Move-Item .\WinPlay\WinPlay-main\ .
Remove-Item .\WinPlay
Rename-Item .\WinPlay-main\ -NewName WinPlay

& .\\.venv\\python.exe -m pip install -r .\\WinPlay\\requirements.txt

Remove-Item .\\WinPlay\\installer -Recurse

Invoke-WebRequest -Uri https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip -OutFile ffmpeg.zip
Expand-Archive .\\ffmpeg.zip
Move-Item .\\ffmpeg\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe .
Remove-Item .\\ffmpeg -Recurse

Invoke-WebRequest -Uri https://download.vb-audio.com/Download_CABLE/VBCABLE_Driver_Pack43.zip -OutFile vbcable.zip
Expand-Archive .\\vbcable.zip
Start-Process .\\vbcable\\VBCABLE_Setup_x64.exe -Wait


New-Item .\\WinPlay.vbs

Set-Content -Path .\\WinPlay.vbs -Value '
Set objShell = CreateObject("WScript.Shell")

pythonExePath = "C:/Program Files/WinPlay/.venv/python.exe"
pythonScriptPath = "C:/Program Files/WinPlay/WinPlay/main.py"

fullCommand = Chr(34) & pythonExePath & Chr(34) & " " & Chr(34) & pythonScriptPath & Chr(34)

objShell.Run fullCommand, 0, False
'

Copy-Item .\\WinPlay "C:\\Program Files\\WinPlay" -Recurse

Copy-Item .\\.venv "C:\\Program Files\\WinPlay\\" -Recurse

Copy-Item .\\ffmpeg.exe "C:\\Program Files\\WinPlay\\"

$current_user_name = [Environment]::UserName

Copy-Item .\\WinPlay.vbs "C:\Users\$current_user_name\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

Set-Location ..

Remove-Item .\\temp -Recurse

Restart-Computer