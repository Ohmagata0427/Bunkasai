@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul && (py start_server.py) || (python start_server.py)
pause
