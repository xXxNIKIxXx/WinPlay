New-Item temp -ItemType Directory
Set-Location .\\temp
Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.5/python-3.12.5-embed-amd64.zip -OutFile python-3.12.5-embed-amd64.zip
Expand-Archive .\\python-3.12.5-embed-amd64.zip
Remove-Item .\\python-3.12.5-embed-amd64.zip
Set-Location .\\python-3.12.5-embed-amd64
Add-Content -Path .\python312._pth -Value 'import site'
Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py
&.\python.exe get-pip.py
Remove-Item get-pip.py
Set-Location ..
Start-Sleep -Seconds 1
Rename-Item .\python-3.12.5-embed-amd64\ .venv

Invoke-WebRequest -Uri https://github.com/xXxNIKIxXx/WinPlay/archive/refs/heads/main.zip -OutFile WinPlay.zip
Expand-Archive .\\WinPlay.zip
Remove-Item .\\WinPlay.zip
Move-Item .\WinPlay\WinPlay-main\ .
Remove-Item .\WinPlay
Rename-Item .\WinPlay-main\ -NewName WinPlay

&.\\.venv\\python.exe -m pip install -r .\\WinPlay\\requirements.

Remove-Item .\\WinPlay\\installer