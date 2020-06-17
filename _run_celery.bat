@echo off
cmd /k "cd /d D:\_My_Projects\karuna\venv\Scripts\ & activate		& cd /d D:\_My_Projects\karuna\ & celery -A core worker -S django --pool=solo -l INFO"
