@echo off
echo ========================================
echo CTools Build Script
echo ========================================
echo.

:: Change to script directory
cd /d "%~dp0"

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    echo Make sure venv exists. Run: python -m venv venv
    pause
    exit /b 1
)

:: Get cterasdk path
echo.
echo Finding cterasdk location...
for /f "delims=" %%i in ('python -c "import cterasdk; import os; print(os.path.dirname(cterasdk.__file__))"') do set CTERASDK_PATH=%%i

if "%CTERASDK_PATH%"=="" (
    echo ERROR: Could not find cterasdk
    echo Make sure cterasdk is installed: pip install cterasdk
    pause
    exit /b 1
)
echo Found cterasdk at: %CTERASDK_PATH%

:: Clean previous build
echo.
echo Cleaning previous build...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist ctools.spec del ctools.spec

:: Run PyInstaller
echo.
echo Building executable...
echo ========================================
pyinstaller --name ctools --onefile --console ^
    --icon=assets\ctools.ico ^
    --add-data "%CTERASDK_PATH%;cterasdk" ^
    --add-data "src\ctools;ctools" ^
    --add-data "assets;assets" ^
    --hidden-import=PySide6.QtWidgets ^
    --hidden-import=PySide6.QtCore ^
    --hidden-import=PySide6.QtGui ^
    --hidden-import=PySide6.QtSvg ^
    --hidden-import=urllib3 ^
    --hidden-import=certifi ^
    --hidden-import=aiohttp ^
    --hidden-import=aiofiles ^
    --hidden-import=cryptography ^
    --hidden-import=yaml ^
    --hidden-import=xml.etree.ElementTree ^
    --hidden-import=xml.dom ^
    --hidden-import=xml.dom.minidom ^
    --hidden-import=packaging ^
    --hidden-import=packaging.version ^
    --hidden-import=snappy ^
    --collect-data=certifi ^
    ctools.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

:: Check if exe was created
if exist dist\ctools.exe (
    echo.
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo Executable: %~dp0dist\ctools.exe
    echo.
    dir dist\ctools.exe
) else (
    echo.
    echo ERROR: ctools.exe was not created
    pause
    exit /b 1
)

echo.
pause
