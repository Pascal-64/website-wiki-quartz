@echo off
echo === Schritt 1: Generieren (Dry-Run) ===
echo content/ wird NICHT veraendert.
echo.
python scripts\wiki_agent_local.py --max-gaps 1 --model qwen2.5-coder:14b
echo.
echo Weiter mit: 2_review.bat
pause
