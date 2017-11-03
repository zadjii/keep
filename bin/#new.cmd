@echo off
setlocal
set _KEEP_ROOT=%~dp0/..
python %_KEEP_ROOT%/keep.py new %*