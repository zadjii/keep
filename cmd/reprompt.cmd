@echo off
@chcp 65001 1> NUL


set GITBRANCH=

FOR /F "tokens=* USEBACKQ" %%F IN (`git symbolic-ref --short HEAD 2^> NUL`) DO (
SET GITBRANCH=%%F
)

if "%GITBRANCH%" == "" (
    PROMPT $e[107;30m[$T]$e[97;46m$P$e[36;49m$e[0m$_$e[0m$e[94m%username%$e[0m@$e[32m%computername%$e[0m$G
) else (
    PROMPT $e[107;30m[$T]$e[97;46m$P$e[36;49m$e[0m$_$e[0m $e[48;5;214m[%GITBRANCH%]$e[0m $e[0m$e[94m%username%$e[0m@$e[32m%computername%$e[0m$G
)

@chcp 437 1> NUL
