@echo off
rem Einfacher Auto-Upload mit Datum

for /f %%i in ('powershell -Command "Get-Date -Format yyyy-MM-dd"') do set datum=%%i

git add .
git commit -m "update %datum%"
git push

pause