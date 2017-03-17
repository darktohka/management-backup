@echo off
title Backup Server
cd ../

:start
python -m backup.ServiceStart
pause
goto start