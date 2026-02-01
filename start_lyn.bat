@echo off
cd /d C:\lyn_ai
timeout /t 30
python lyn_voice.py >> lyn.log 2>&1
