@echo off
setlocal
cd /d "%~dp0"
py -3 -c "import sys, tkinter; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 (
  echo Install Python 3.10 or newer for Windows from https://www.python.org/downloads/windows/
  echo Include the py launcher and Tcl/Tk. Then open this file again.
  echo Read docs/QUICK_START.md for complete instructions.
  pause
  exit /b 1
)
py -3 "%~dp0patch_gui.py" --language en
if errorlevel 1 pause
