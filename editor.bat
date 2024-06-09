@echo off

call %~dp0\vars.bat

start  "%UE4EDITOR_EXE%" "%UPROJECT_PATH%" %*