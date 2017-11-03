@echo off
@rem The contents of this file should be the same in both #go and +
python %~dp0/keep.py go %*

FOR /F "tokens=* USEBACKQ" %%F IN (`python %~dp0/keep.py go %* 2^> NUL`) DO (
    set __target_dir__=%%F
)
vf %__target_dir__%