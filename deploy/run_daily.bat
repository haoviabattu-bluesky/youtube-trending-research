@echo off
REM Chay hang ngay tren may nha qua Windows Task Scheduler.
REM Log ghi kem ngay, giu lai de truy nguoc khi bao cao sai.
cd /d "%~dp0.."
set PYTHONIOENCODING=utf-8
for /f "tokens=1-3 delims=/- " %%a in ("%date%") do set TODAY=%%c%%b%%a
py -3.13 -X utf8 src\run_daily.py %* >> "data\daily_%TODAY%.log" 2>&1
exit /b %ERRORLEVEL%
