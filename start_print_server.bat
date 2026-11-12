@echo off
title ZStore Print Server for Xprinter XP-365B
echo ===================================================
echo     ZStore Print Server for Xprinter XP-365B
echo ===================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ПОМИЛКА] Python не встановлено або не додано у PATH!
    echo Завантажте Python з https://www.python.org/ і при встановленні обов'язково
    echo поставте галочку "Add python.exe to PATH".
    echo.
    pause
    exit /b 1
)

echo Перевірка необхідних бібліотек...
pip install --quiet pillow pywin32

echo Запуск сервера друку...
python print_server_win.py
pause
