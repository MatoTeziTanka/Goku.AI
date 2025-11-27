@echo off
echo ========================================
echo   Goku.AI Uninstallation (Windows)
echo ========================================
echo.
set /p confirm="Are you sure? (yes/no): "
if /i not "%confirm%"=="yes" (
    echo Uninstallation cancelled.
    pause
    exit /b
)
echo Uninstalling...
pip uninstall -r ..\..\requirements.txt -y
echo.
echo ✅ Uninstallation complete!
pause
