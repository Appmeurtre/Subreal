@echo off

set ROOTDIR=%~dp0
set ROOTDIR=%ROOTDIR:~0, -1%

rem #Enter Project Name in here
set PROJECT=Subreal
set PROJECT_DIR=%ROOTDIR%\%PROJECT%
set UPROJECT_PATH=%PROJECT_DIR%\%PROJECT%.uproject

rem #Enter your Unreal Engine Root here
set UE5_DIR=C:\Program Files\Epic Games\UE_5.3

rem #Warning! Unreal Engine 4 & 5 uses different names for Editor.exe, check if yours is named UnrealEditor.exe
set UE5EDITOR_EXE=%UE5_DIR%\Engine\Binaries\Win64\UnrealEditor.exe
set BUILD_BAT=%UE5_DIR%\Engine\Build\BatchFiles\Build.bat