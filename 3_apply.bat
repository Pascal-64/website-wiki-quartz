@echo off
echo === Schritt 3: Run auswaehlen und anwenden ===
echo Zeigt alle verfuegbaren Runs mit Metriken.
echo Du waehlst welchen Run angewendet werden soll.
echo.
python scripts\wiki_apply_run.py
echo.
echo Wenn der Diff oben gut aussieht: 4_commit_push.bat
echo Wenn nicht: git checkout content\  (macht Aenderung rueckgaengig)
pause
