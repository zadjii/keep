@echo off
setlocal
set KEEP_ROOT=%~dp0/..
python %KEEP_ROOT%/keep.py name %*
