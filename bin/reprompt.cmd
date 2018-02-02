@echo off
@chcp 65001 1> NUL


@rem This is your seperator character
@rem    Most fonts don't support the first one, it's a powerline character
@rem    If it's not supported, try another

rem set _seperator=
set _seperator=$g

set GITBRANCH=

FOR /F "tokens=* USEBACKQ" %%F IN (`git symbolic-ref --short HEAD 2^> NUL`) DO (
SET GITBRANCH=%%F
)

rem set _GITPROMPT=

if "%GITBRANCH%" == "" (
    set _GITPROMPT=$e[0m
) else (
    rem set "_GITPROMPT= $e[48;5;214m[%GITBRANCH%]$e[0m "
    set "_GITPROMPT= $e[43;37m[%GITBRANCH%]$e[0m "
)

if "%_BuildAlt%" == "" (
    set "_razPROMPT="
) else (
    set "_razPROMPT= [%_BuildAlt%] "
)

if "%KEEP_WORKSPACE%" == "" (
    set "_KEEP_WORKSPACE_PROMPT="
) else (
    set "_KEEP_WORKSPACE_PROMPT=$e[35;40m[%KEEP_WORKSPACE%]$e[m"
)

PROMPT $e[107;30m%_razPROMPT%[$T]$e[97;46m%_seperator%$P$e[36;49m%_seperator%$e[0m$_$e[0m%_KEEP_WORKSPACE_PROMPT%%_GITPROMPT%$e[94m%username%$e[0m@$e[32m%computername%$e[0m$G

@rem Hey you. Working on a MinwinPC machine? %username% is actually "MINWINPC$" there.
@rem use this instead:
@rem PROMPT $e[107;30m[$T]$e[97;46m$G$P$e[36;49m$G$e[0m$_$e[94m%username%e[0m@$e[32m%computername%$e[0m$G


@chcp 437 1> NUL
