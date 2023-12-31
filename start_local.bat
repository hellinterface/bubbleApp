@echo off

echo %1

IF %1 == -int GOTO Internal
IF %1 == -ext GOTO External
IF %1 == . GOTO External

:External
    echo "Starting external..."
    echo %cd%
    uvicorn app_external.main:app --reload --port 443 --host bubble.net --ssl-keyfile="bubble.key" --ssl-certfile="bubble.crt"
:Internal
    echo "Starting internal..."
    echo %cd%
    uvicorn app_internal.main:app --reload --port 8080

REM uvicorn main:app --reload --port 8080 --host 192.168.1.3 --ssl-keyfile='rtcom.key' --ssl-certfile='rtcom.crt'
