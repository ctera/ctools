Set-Location 'c:\Users\lakea\Desktop\CTERA\ctools'

# Get cterasdk path using venv Python
$cterasdk_path = & 'c:\Users\lakea\Desktop\CTERA\ctools\venv\Scripts\python.exe' -c "import cterasdk; import os; print(os.path.dirname(cterasdk.__file__))"
Write-Host "cterasdk path: $cterasdk_path"

# Clean previous build
if (Test-Path dist) { Remove-Item -Recurse -Force dist }
if (Test-Path build) { Remove-Item -Recurse -Force build }
if (Test-Path ctools.spec) { Remove-Item -Force ctools.spec }

# Run PyInstaller
& 'c:\Users\lakea\Desktop\CTERA\ctools\venv\Scripts\pyinstaller.exe' `
    --name ctools --onefile --console `
    --add-data "$cterasdk_path;cterasdk" `
    --add-data "src\ctools;ctools" `
    --add-data "assets;assets" `
    --hidden-import=PySide6.QtWidgets `
    --hidden-import=PySide6.QtCore `
    --hidden-import=PySide6.QtGui `
    --hidden-import=urllib3 `
    --hidden-import=certifi `
    --hidden-import=aiohttp `
    --hidden-import=aiofiles `
    --hidden-import=cryptography `
    --hidden-import=yaml `
    --hidden-import=xml.etree.ElementTree `
    --hidden-import=xml.dom `
    --hidden-import=xml.dom.minidom `
    --hidden-import=packaging `
    --hidden-import=packaging.version `
    --hidden-import=snappy `
    --collect-data=certifi `
    ctools.py

# Check result
if (Test-Path dist\ctools.exe) {
    Write-Host "BUILD SUCCESSFUL!"
    Get-Item dist\ctools.exe
} else {
    Write-Host "BUILD FAILED!"
    exit 1
}
