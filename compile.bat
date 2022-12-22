@echo off
title DB Manager - Compile
echo Welcome to DB Manager compiler.
echo[
:AskForPyInstaller
echo[
echo Do you have "pyinstaller" python module installed in your computer? (Y/N)
set /p PyInstallerAnswer=
if %PyInstallerAnswer%==y goto StartCompiling
if %PyInstallerAnswer%==n goto InstallPyInstaller
goto AskForPyInstaller
:InstallPyInstaller
echo [+] Installing module pyinstaller...
echo[
pip install pyinstaller
echo[
:StartCompiling
echo [+] Compiling....
echo[
cd ./src/
pyinstaller -i "../logo.png" -n "DB Manager" -F main.py
echo[
echo [+] Done. Check this directory: src/dist/
PAUSE