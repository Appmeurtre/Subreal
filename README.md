# 🎮 Subreal Engine Console GUI

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/Unreal%20Engine-4.27%2B%20%7C%205.x-0E1128?style=for-the-badge&logo=unrealengine&logoColor=white" alt="Unreal Engine">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-4285F4?style=for-the-badge" alt="Cross Platform">
  <img src="https://img.shields.io/badge/License-GPL%20v3-yellow?style=for-the-badge" alt="GPLv3 License">
</div>

<div align="center">
  <h3>🚀 Professional Console-Based Project Management for Unreal Engine</h3>
  <p><strong>A comprehensive Python-based GUI tool for managing Unreal Engine projects without heavyweight IDEs</strong></p>
</div>

---

## 🎯 About

**Subreal Engine Console GUI** is my personal solution to the bloat and complexity of modern IDEs. After years of fighting with Visual Studio's sluggish performance and overwhelming interface, I decided to build something better—a lightweight, fast, and intuitive terminal-based tool for Unreal Engine development.

This project represents my philosophy: **powerful tools don't need to be heavy**. Built with Python and featuring a carefully crafted orange-themed interface, it provides everything you need for professional Unreal Engine development without the IDE overhead.

### Why I Built This
- **🚫 No More Bloat**: Tired of waiting for Visual Studio to load, index, and respond
- **⚡ Instant Performance**: Python application that starts immediately and stays responsive
- **🎨 Thoughtful Design**: Every interface element designed for efficiency and clarity
- **🔧 Complete Solution**: All essential tools in one cohesive, well-integrated package
- **🛡️ Professional Quality**: Enterprise-grade safety features with automatic backups
- **📦 Clean Architecture**: Monolithic design that's easy to understand and maintain

## ✨ Key Features

### 🏗️ **Project Management**
- **Project Building**: Visual progress tracking with detailed error reporting
- **Editor Launch**: Direct Unreal Editor launching with validation
- **Project Information**: Comprehensive project analysis and path validation
- **Directory Management**: Quick access to project folders and files

### 🔧 **Advanced Project Renaming**
- **Smart Detection**: Automatically identifies Blueprint-only vs C++ projects
- **Safe Renaming**: Creates backups before any modifications
- **C++ Support**: Handles source files, headers, modules, and build configurations
- **Blueprint Support**: Simple renaming with configuration updates
- **Validation**: Comprehensive name validation with helpful warnings
- **Rollback**: Automatic restoration if renaming fails

### 🧹 **Project Cleanup**
- **Intelligent Scanning**: Identifies build cache, temporary files, and artifacts
- **Safe Removal**: Only deletes regenerable files and directories
- **Size Analysis**: Shows disk space that will be freed
- **Backup Creation**: Optional backup lists for recovery
- **Category-Based**: Organized cleanup by file type and importance

### ⚙️ **Engine Configuration**
- **Path Management**: Easy Unreal Engine installation path configuration
- **Version Handling**: Support for multiple UE versions
- **Validation**: Automatic path and installation verification
- **Cross-Platform**: Windows and macOS support with platform-specific optimizations

### 🎨 **User Experience**
- **Intuitive Navigation**: Arrow keys, WASD controls, and browser-style history
- **Visual Feedback**: Progress bars, colored status indicators, and clear messaging
- **Error Handling**: Comprehensive error reporting with troubleshooting hints
- **Professional Design**: Consistent branding and polished interface elements

## 🔧 Technical Architecture

### **Modern Python Design**
- **Object-Oriented**: Clean class-based architecture with separation of concerns
- **Modular Structure**: Vendor modules for colors, icons, project operations
- **Type Safety**: Type hints and validation throughout
- **Error Resilience**: Comprehensive exception handling and recovery

### **Cross-Platform Compatibility**
- **Windows**: Native console integration with proper ANSI support
- **macOS**: Terminal.app compatibility with Unix-style navigation
- **Python 3.7+**: Modern Python features with backward compatibility

### **Professional Code Quality**
- **Documentation**: Comprehensive docstrings and inline comments
- **Standards**: PEP 8 compliant code with consistent formatting
- **Testing**: Built-in validation and error simulation
- **Maintenance**: Easy to extend and modify codebase

## 📋 Requirements

| Component | Version | Platform |
|-----------|---------|----------|
| **Python** | 3.7+ | Windows, macOS |
| **Unreal Engine** | 4.27+ or 5.x | Any supported platform |
| **Operating System** | Windows 10/11, macOS 10.15+ | |
| **Terminal** | Windows Console, Terminal.app | Platform native |

## 🚀 Quick Start

### **Instant Launch**
```bash
# Windows - Double-click
Subreal_GUI.bat

# macOS - Double-click  
Subreal_GUI.command

# Manual launch (any platform)
python subreal_gui.py
```

### **First-Time Setup**
1. **Launch Application**: Use platform-appropriate launcher
2. **Initial Configuration**: Choose default or custom configuration
3. **Path Validation**: Application validates all paths automatically
4. **Ready to Use**: Start building and managing projects immediately

## 🏗️ Project Structure

```
subreal/
├── 📄 subreal_gui.py           # Main application with integrated functionality
├── 📂 vendor/                  # Modular component library
│   ├── 🎨 colors.py           # Terminal color management
│   ├── 🔧 icons.py            # Cross-platform icon system  
│   ├── 🧹 cleaner.py          # Project cleanup utilities
│   └── 🔄 project_renamer.py  # Advanced renaming engine
├── 🚀 Subreal_GUI.bat         # Windows double-click launcher
├── 🚀 Subreal_GUI.command     # macOS double-click launcher
├── 📖 README.md               # This documentation
└── 📂 Subreal/                # Example Unreal Engine project
    ├── Config/                # Engine configuration
    ├── Content/               # Game assets
    ├── Source/                # C++ source code
    └── Subreal.uproject       # Project file
```

## 💻 Advanced Usage

### **Project Renaming Workflow**
```bash
1. Analysis     → Detect project type (Blueprint/C++)
2. Validation   → Verify new name and show warnings
3. Confirmation → Review changes and create backup
4. Execution    → Rename files, update references
5. Verification → Validate results and cleanup
```

### **Cleanup Categories**
- **Temporary Cache**: Build cache, intermediate files
- **Build Artifacts**: Compiled binaries, debug files  
- **IDE Files**: Generated project files
- **UE Generated**: Engine logs, crashes, profiling data
- **Asset Cache**: Cooked assets, shader cache

### **Keyboard Shortcuts**
| Key | Action |
|-----|--------|
| `↑↓` or `WS` | Navigate menu items |
| `Enter` | Select/Execute |
| `ESC` | Back/Cancel |
| `←→` | History navigation |

## 🛠️ Development Highlights

This project demonstrates several advanced development practices:

### **Software Architecture**
- **Single Responsibility**: Each module handles one specific domain
- **Dependency Injection**: Configuration and utilities passed to components
- **State Management**: Clean separation of UI state and business logic
- **Error Boundaries**: Isolated error handling with graceful degradation

### **User Experience Design**
- **Progressive Enhancement**: Features unlock based on project complexity
- **Defensive Programming**: Validates all user input and system state
- **Accessibility**: Keyboard-only navigation with visual indicators
- **Responsive Design**: Adapts to different terminal sizes and capabilities

### **Code Quality Practices**
- **Type Safety**: Comprehensive type hints and validation
- **Documentation**: Self-documenting code with clear naming
- **Testing**: Built-in validation and error simulation
- **Maintenance**: Modular design for easy extension and modification

## 🎓 Portfolio Showcase

This project showcases:

- **✅ Full-Stack Development**: Complete application from UI to business logic
- **✅ Cross-Platform Programming**: Windows and macOS compatibility
- **✅ File System Operations**: Safe file manipulation with backup/restore
- **✅ Process Management**: External process launching and monitoring
- **✅ Configuration Management**: JSON-based settings with validation
- **✅ User Interface Design**: Terminal-based GUI with professional polish
- **✅ Error Handling**: Comprehensive exception management and recovery
- **✅ Documentation**: Professional README and inline documentation
- **✅ Code Organization**: Clean architecture with modular design
- **✅ Version Control**: Git best practices with meaningful commits

## 🤝 Contributing

This is a portfolio project, but suggestions and feedback are welcome! The codebase is designed to be easily extensible and well-documented for learning purposes.

## 📜 License

This project is licensed under the GPL v3 License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <p><strong>Built with 🧡 by Yılmaz Seyhan</strong></p>
  <p><em>"Why use bloated IDEs when you can build something better?"</em></p>
  <p>🚀 <strong>Lightweight tools for serious developers</strong></p>
</div>