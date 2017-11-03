@echo off
@chcp 65001 1> NUL


set GITBRANCH=

FOR /F "tokens=* USEBACKQ" %%F IN (`git symbolic-ref --short HEAD 2^> NUL`) DO (
SET GITBRANCH=%%F
)

rem set _GITPROMPT=

if "%GITBRANCH%" == "" (
    set _GITPROMPT=$e[0m
) else (
    set "_GITPROMPT= $e[48;5;214m[%GITBRANCH%]$e[0m "
)

if "%_BuildAlt%" == "" (
    set "_razPROMPT="
) else (
    set "_razPROMPT= [%_BuildAlt%] "
)

PROMPT $e[107;30m%_razPROMPT%[$T]$e[97;46m$P$e[36;49m$e[0m$_$e[0m%_GITPROMPT%$e[94m%username%$e[0m@$e[32m%computername%$e[0m$G


@chcp 437 1> NUL