@echo off

set KEEP_ROOT=%~dp0/..

if "%1" == "" (
    @rem do nothing
    python %KEEP_ROOT%/keep.py work
    goto :END
) else (
    set KEEP_WORKSPACE=%1
)

setlocal enabledelayedexpansion

set _found_dir=0
set _found_cmd=0

set "__target_dir__="
set "__target_cmd__="

FOR /F "tokens=* USEBACKQ" %%F IN (`python %KEEP_ROOT%/keep.py work %* 2^> NUL`) DO (

    if !_found_dir! == 0 (
        set __target_dir__=%%F
        set _found_dir=1
    ) else (
        if !_found_cmd! == 0 (
            set __target_cmd__=%%F
            set _found_cmd=1
            goto :post_process_output
        )
    )
)

:post_process_output

echo HEY so it seems as though if we execute the command before we endlocal, then env variables that the commad executes wont get set. cha feel? gotta find a way to do both.

if !_found_cmd! == 1 (
    set real = !__target_cmd__!
    if !_found_dir! == 1 (
        rem endlocal 
        call %KEEP_ROOT%\bin\vf.cmd %__target_dir__%
    ) 
    !__target_cmd__!
    rem %real%
)
@rem For some reason, If you don't endlocal before calling vf,
@rem    it won't change dirs, and the title bar will get modified.
@rem    So do this weird endlocal twice thing.
if !_found_dir! == 1 (
    endlocal 
    call %KEEP_ROOT%\bin\vf.cmd %__target_dir__%
) 

endlocal
set "_found_dir="
set "_found_cmd="
set "__target_dir__="
set "__target_cmd__="

:END
