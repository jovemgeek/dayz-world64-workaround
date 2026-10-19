@echo off
setlocal
cd /d "%~dp0"
py -3 -c "import sys, tkinter; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 (
  echo Instale Python 3.10 ou superior para Windows em https://www.python.org/downloads/windows/
  echo Inclua o launcher py e Tcl/Tk na instalacao. Depois abra este arquivo novamente.
  echo Leia README.pt-BR.md para as instrucoes completas.
  pause
  exit /b 1
)
py -3 "%~dp0patch_gui.py" --language pt
if errorlevel 1 pause
