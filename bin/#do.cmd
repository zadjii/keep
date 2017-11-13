@echo off
set KEEP_ROOT=%~dp0/..

@rem The contents of this file should be the same in both #go and +
if "%1" == "" (
    @rem do nothing
    python %KEEP_ROOT%/keep.py do
    goto :END

) else (

    call :get_params %*

    call :do_init
    @rem have to use call on the above line to get the title to reset I guess.
)
goto :END

:get_params
setlocal enabledelayedexpansion

FOR /F "tokens=* USEBACKQ" %%F IN (`python %KEEP_ROOT%/keep.py do %* 2^> NUL`) DO (
    echo %%F
    set __target_cmd__=%%F
    goto :end_get_params

)
:end_get_params
endlocal & set "_target_cmd_=%__target_cmd__%"
goto :END


:do_init 
call %_target_cmd_%
goto :END

:END
