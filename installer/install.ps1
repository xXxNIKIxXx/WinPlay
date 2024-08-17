New-Item temp
Set-Location .\\temp
Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.5/python-3.12.5-embed-amd64.zip -OutFile python-3.12.5-embed-amd64.zip
Expand-Archive .\\python-3.12.5-embed-amd64.zip
Remove-Item .\\python-3.12.5-embed-amd64.zip
Set-Location .\\python-3.12.5-embed-amd64
Add-Content -Path .\python312._pth -Value 'import site'
Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py
.\python.exe get-pip.py
Rename-Item . .venv_test