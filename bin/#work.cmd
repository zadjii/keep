@echo off

set KEEP_ROOT=%~dp0/..

if "%1" == "" (
    @rem do nothing
    python %KEEP_ROOT%/keep.py work
    goto :END
) else (
    set KEEP_WORKSPACE=%1
)

call :get_params %*

@rem if there is a commnand vf then do it.
@rem else just vf.
if %_found_cmd% == 1 (
    if %_found_dir% == 1 (
        call %KEEP_ROOT%\bin\vf.cmd %_target_dir_%
    ) 
    %_target_cmd_%
) else (
    if %_found_dir% == 1 (
        call %KEEP_ROOT%\bin\vf.cmd %_target_dir_%
    )
) 

goto :END

@rem see https://ss64.com/nt/syntax-functions.html
@rem    This has to be packaged up as a function, so that the setlocal/endlocal 
@rem    is contained, and we can return out our variables.
:get_params
setlocal enabledelayedexpansion

set _found_dir=0
set _found_cmd=0

set "__target_dir__="
set "__target_cmd__="

FOR /F "tokens=* USEBACKQ" %%F IN (`python %KEEP_ROOT%/keep.py work %* 2^> NUL`) DO (
    echo %%F
    if !_found_dir! == 0 (
        set __target_dir__=%%F
        set _found_dir=1
    ) else (
        if !_found_cmd! == 0 (
            set __target_cmd__=%%F
            set _found_cmd=1
            goto :end_get_params
        )
    )
)
:end_get_params
endlocal & set _target_dir_=%__target_dir__% & set _target_cmd_=%__target_cmd__% & set _found_dir=%_found_dir% & set _found_cmd=%_found_cmd% 


:END
