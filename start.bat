@echo off

set PYTHON_EXECUTABLE=py
set VENV_DIR=venv

if not exist %VENV_DIR% (
    echo No venv found, creating one
    %PYTHON_EXECUTABLE% -m venv %VENV_DIR%

    echo Installing dependencies via pip
    call %VENV_DIR%\Scripts\activate.bat
    %PYTHON_EXECUTABLE% -m pip install -r requirements.txt
)

mkdir data\img_orig
mkdir data\res\image
mkdir data\res\thumb
mkdir data\res\avatar
xcopy /Y src\js data\res\js /s /e /h
xcopy /Y src\css data\res\css /s /e /h
xcopy /Y src\img data\res\img /s /e /h

call %VENV_DIR%\Scripts\activate.bat
%PYTHON_EXECUTABLE% modules\main.py
