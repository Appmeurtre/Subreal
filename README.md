# 🎮 Subreal Engine

<div align="center">
  <img src="https://img.shields.io/badge/Unreal%20Engine-5.3-blue?style=for-the-badge&logo=unrealengine" alt="Unreal Engine 5.3">
  <img src="https://img.shields.io/badge/C%2B%2B-14.34+-00599C?style=for-the-badge&logo=cplusplus" alt="C++">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows" alt="Windows">
  <img src="https://img.shields.io/badge/License-GPL%20v3-yellow?style=for-the-badge" alt="GPLv3 License">
</div>

<div align="center">
  <h3>🚀 IDE-Free Unreal Engine Development Setup</h3>
  <p><strong>Develop Unreal Engine projects with your favorite text editor - no Visual Studio required!</strong></p>
</div>

---

## 📋 Table of Contents
- [About](#-about)
- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Batch Commands](#-batch-commands)
- [Creating a Project from Scratch](#-creating-a-project-from-scratch)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Credits](#-credits)

## 🎯 About

**Subreal Engine** is a lightweight development setup that eliminates the need for heavyweight IDEs when working with Unreal Engine. Named after Sublime Text (but compatible with any text editor), this setup provides a streamlined workflow for C++ game development.

### Why Subreal?
- **🚀 Fast**: No IDE overhead - compile and run directly
- **🎨 Flexible**: Use ANY text editor you prefer
- **📦 Minimal**: Only essential tools required
- **⚡ Efficient**: Batch scripts for common operations
- **🔧 Customizable**: Easy to adapt to your workflow

## ✨ Features

- **IDE-Independent Development**: Write code in Sublime Text, VS Code, Vim, or any editor
- **Automated Build System**: Simple batch scripts for building and launching
- **Module-Based Architecture**: Clean separation of game modules
- **Perforce Integration**: Pre-configured `.p4ignore` for version control
- **Git LFS Support**: Optimized for large binary assets
- **Custom Logging System**: Built-in logging infrastructure
- **Hot Reload Support**: Iterate quickly without editor restarts

## 🔧 Requirements

### Core Requirements
| Component | Version | Required |
|-----------|---------|----------|
| MSVC Compiler for C++ | 14.34.31933+ | ✅ |
| Windows 10 SDK | 10.0.18362.0+ | ✅ |
| LLVM Clang | 14.0.1 | ✅ |
| .NET Framework | 4.6.2 Targeting Pack | ✅ |
| .NET | 6.0 | ✅ |
| Visual Studio | 2022 v17.4+ | ⚠️ Optional |
| Unreal Engine | 5.3 | ✅ |

### Recommended Editor Extensions

#### 🔵 Visual Studio Code
```bash
code --install-extension CAPTNCAPS.ue4-snippets
```

#### 🟣 Sublime Text
```bash
Package Control: Install Package > Unreal Snippets
```

## 📥 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/subreal-engine.git
cd subreal-engine
```

### 2. Configure Environment
Edit `vars.bat` to match your Unreal Engine installation:
```batch
rem Update this line with your UE5 installation path
set UE5_DIR=C:\Program Files\Epic Games\UE_5.3
```

### 3. Build the Project
```bash
build.bat
```

### 4. Launch the Editor
```bash
editor.bat
```

## 🚀 Quick Start

```bash
# 1. Build the project
build.bat

# 2. Open in Unreal Editor
editor.bat

# 3. Start coding in your favorite editor!
```

## 📁 Project Structure

```
Subreal/
├── 📂 Config/              # Engine and game configuration
│   ├── DefaultEngine.ini
│   ├── DefaultGame.ini
│   └── DefaultInput.ini
├── 📂 Content/             # Game assets (tracked by Git LFS)
│   └── Maps/
│       └── SubrealMap.umap
├── 📂 Source/              # C++ source code
│   ├── Subreal.Target.cs
│   ├── SubrealEditor.Target.cs
│   └── SubrealCore/        # Primary game module
│       ├── Public/
│       │   └── SubrealCore.h
│       ├── Private/
│       │   ├── SubrealCore.cpp
│       │   ├── Log.h
│       │   └── Log.cpp
│       └── SubrealCore.Build.cs
├── 📄 Subreal.uproject     # Unreal project file
├── 📄 .gitignore           # Git ignore rules
├── 📄 .gitattributes       # Git LFS configuration
└── 📄 .p4ignore            # Perforce ignore rules
```

## 🛠️ Batch Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `build.bat` | Compile the project | `build.bat` |
| `editor.bat` | Launch Unreal Editor | `editor.bat [optional_args]` |
| `vars.bat` | Environment variables | Automatically called by other scripts |

## 🏗️ Creating a Project from Scratch

### Step-by-Step Guide

1. **Create Project Directory**
   ```bash
   mkdir MyGame
   cd MyGame
   ```

2. **Create Project File** (`MyGame.uproject`)
   ```json
   {
     "FileVersion": 3,
     "EngineAssociation": "5.3",
     "Modules": [
       {
         "Name": "MyGameCore",
         "Type": "Runtime",
         "LoadingPhase": "Default"
       }
     ]
   }
   ```

3. **Setup Source Structure**
   ```bash
   mkdir Source
   cd Source
   ```

4. **Create Target Files**
   - `MyGame.Target.cs` (Game target)
   - `MyGameEditor.Target.cs` (Editor target)
   - `MyGameServer.Target.cs` (Optional: Server target)

5. **Create Primary Module**
   ```bash
   mkdir MyGameCore
   cd MyGameCore
   mkdir Public Private
   ```

6. **Add Module Files**
   - `MyGameCore.Build.cs` - Build configuration
   - `Public/MyGameCore.h` - Module header
   - `Private/MyGameCore.cpp` - Module implementation
   - `Private/Log.h` - Logging header
   - `Private/Log.cpp` - Logging implementation

## 🔍 Troubleshooting

### Batch Files Not Working?
```batch
rem Verify your paths in vars.bat:
set UE5_DIR=YOUR_UNREAL_ENGINE_PATH
set UE5EDITOR_EXE=%UE5_DIR%\Engine\Binaries\Win64\UnrealEditor.exe
```

### Different Unreal Engine Version?
Check the [Platform SDK Requirements](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5.3-release-notes) for your version.

### Source-Built Engine?
Update `vars.bat` with your custom engine location.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👏 Credits

- **Yılmaz Seyhan** - Creator and Maintainer
- **Alex Forsythe** - Original inspiration for IDE-free workflow

---

<div align="center">
  <p><strong>Made with ❤️ by ylmz</strong></p>
  <p>Istanbul, Turkey 🇹🇷</p>
</div>
