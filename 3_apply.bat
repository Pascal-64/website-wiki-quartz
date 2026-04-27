@echo off
echo === Schritt 3: Patch anwenden ===
echo Wendet den neuesten generierten Abschnitt auf content/ an.
echo.
python scripts\wiki_apply_latest.py
echo.
echo Wenn der Diff oben gut aussieht: 4_commit_push.bat
echo Wenn nicht: git checkout content\  (macht Aenderung rueckgaengig)
pause
