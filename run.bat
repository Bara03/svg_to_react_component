@echo off
setlocal

REM Set the path to your Python executable
set PYTHON_PATH=python

REM Check if required Python libraries are available, if not, install them
%PYTHON_PATH% -c "import xml.etree.ElementTree" 2>nul || (
    echo Installing required libraries...
    %PYTHON_PATH% -m pip install xml.etree.ElementTree
)

%PYTHON_PATH% -c "import pyperclip" 2>nul || (
    echo Installing required libraries...
    %PYTHON_PATH% -m pip install pyperclip
)

REM Run the Python script
%PYTHON_PATH% extractsvg.py

pause
