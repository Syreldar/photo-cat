@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."
chcp 65001 >nul
mode con: cols=128 lines=42
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0fix_console_window.ps1" -Columns 128 -Lines 42 >nul 2>nul
title PHOTO-CAT Pipeline

echo ============================================================
echo PHOTO-CAT - Pipeline
echo ============================================================
echo Project folder: %CD%
echo Configuration:  %CD%\config.yaml
echo.

if not exist ".venv\Scripts\python.exe" (
    echo The local virtual environment was not found.
    echo.
    echo Run START_WINDOWS.bat first.
    echo.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" "src\config_and_run.py"
set "EXIT_CODE=%ERRORLEVEL%"

echo.
echo ============================================================
if "%EXIT_CODE%"=="0" (
    echo PHOTO-CAT completed successfully.
    echo Check the output folder for results.
) else (
    echo PHOTO-CAT stopped because of an error.
    echo Read the message above, fix the configuration, then try again.
)
echo ============================================================
echo.
echo Press any key to close this window.
pause >nul
exit /b %EXIT_CODE%
