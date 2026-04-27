@echo off
echo === Schritt 2: Generated.md pruefen ===
echo.
for /f "delims=" %%i in ('powershell -NoProfile -Command "Get-ChildItem -Path '.runs\wiki-agent' -Recurse -Filter 'generated.md' 2>$null | Sort-Object LastWriteTime -Descending | Select-Object -First 1 -ExpandProperty FullName"') do (
    echo Oeffne: %%i
    start "" "%%i"
    goto :found
)
echo Keine generated.md gefunden. Zuerst 1_dry_run.bat ausfuehren.
goto :end
:found
echo.
echo Wenn der Inhalt gut aussieht: 3_apply.bat
echo Wenn nicht gut: 1_dry_run.bat nochmal ausfuehren
:end
pause
