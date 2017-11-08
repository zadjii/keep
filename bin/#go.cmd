@echo off
setlocal
set KEEP_ROOT=%~dp0/..

@rem The contents of this file should be the same in both #go and +
python %KEEP_ROOT%/keep.py go %*

FOR /F "tokens=* USEBACKQ" %%F IN (`python %KEEP_ROOT%/keep.py go %* 2^> NUL`) DO (
    set __target_dir__=%%F
)
endlocal & call vf %__target_dir__%
@rem have to use call on the above line to get the title to reset I guess.
