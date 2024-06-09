
# Subreal Engine

This is a Unreal Engine Development setup which eliminates to need for a Integrated Development Environment (IDE). I call this Subreal because I mainly use this with Sublime Text but you can use code editor of your choice.


## Requirements

- MSVC compiler for C++ 14.34.31933 or newer
- Windows 10 SDK (10.0.18362.0) or newer
- LLVM clang 14.0.1
- .NET 4.6.2 Targeting Pack
- .NET 6.0
- Visual Studio 2022 v17.4 or newer (Optional)


## Recommended 

Unreal Engine 4 Snippets for
- [Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=CAPTNCAPS.ue4-snippets)
- [Sublime Text](https://packagecontrol.io/packages/Unreal%20Snippets)


## FAQ

#### Could you use it with other Unreal Engine versions?

Yes but you need to make some tweaks to work, each version of Unreal has different SDK requirements and you can check them under "**Platform SDK Upgrades**" at release notes of the engine version you are using. For this project I based it on [UE 5.3](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5.3-release-notes)

#### Batch Files Does nothing?

If you've compiled Unreal Engine from source insted downloading directly from EpicGames Store, your unreal files may located at somewhere else, you can check the "vars.bat" file to ensure directories are correct for your setup. Also this is only windows.


## Project from Scratch

Example setup steps for creating a new Unreal C++ project from scratch:

- Create a root Unreal project directory: replace Project with your project name
- Add Project.uproj, run uuproj, populate with primary module name (e.g. ProjectCore)
- Add a Source directory
- Within that directory, add Project.Target.cs, run umt, enter primary module name
- Add ProjectEditor.Target.cs the same way, set Type to TargetType.Editor
- If desired, add ProjectServer.Target.cs, set Type to TargetType.Server
- Add a subdirectory for the primary module, e.g. ProjectCore
- Within that directory, add ProjectCore.Build.cs, run umb
- Add two subdirectories, Public and Private
- Within Public, add ProjectCore.h, run umh
- Within Private, add ProjectCore.cpp, run umcp
- Within Private, add Log.h, run ulh
- Within Private, add Log.cpp, run ulc

Thanks for Alex Forsythe to be insparation.

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)


