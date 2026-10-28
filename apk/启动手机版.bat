@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "PY=C:\Users\71097\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
if not exist "%PY%" set "PY=python"
"%PY%" "%~dp0手机服务.py"
pause
