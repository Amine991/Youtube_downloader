@echo off
chcp 65001 >nul
set /p URL=Paste YouTube video or playlist URL: 
python "%~dp0yt_playlist.py" "%URL%" %*
pause
