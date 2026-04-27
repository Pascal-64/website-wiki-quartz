@echo off
echo === Schritt 4: Committen und pushen ===
echo.
git add content\
git status
echo.
set /p MSG=Commit-Message (Enter = Standard):
if "%MSG%"=="" set MSG=Add wiki content
git commit -m "%MSG%"
git push
echo.
echo Fertig! Naechsten Gap starten: 1_dry_run.bat
pause
