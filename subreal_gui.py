#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import platform
import time
from pathlib import Path
from typing import Dict

# Add vendor directory to path for bundled libraries
vendor_path = Path(__file__).parent / "vendor"
if str(vendor_path) not in sys.path:
    sys.path.insert(0, str(vendor_path))

# Import bundled libraries
from colors import orange, bright_orange, dark_orange, light_orange, bold, underline, bright_white, color_manager
from icons import icons, build_icon, editor_icon, project_icon, settings_icon, config_icon, exit_icon
from icons import success_icon, error_icon, warning_icon, back_icon, forward_icon, pointer_icon, clean_icon, trash_icon
from cleaner import ProjectCleaner
from project_renamer import ProjectRenamer

# Platform-specific imports
if platform.system().lower() == "windows":
    import msvcrt
else:
    import termios
    import tty

class SubrealGUI:
    def __init__(self):
        self.script_dir = Path(__file__).parent.resolve()
        self.config_file = self.script_dir / "subreal_config.json"
        self.platform_name = platform.system().lower()
        self.config = self.load_config()
        self.current_selection = 0
        self.menu_items = []
        self.in_submenu = False
        # Browser-like navigation history
        self.navigation_history = []
        self.history_index = -1
        self.current_menu = None
        
    def load_config(self):
        """Load configuration from JSON file or create default"""
        default_config = self.get_default_config()
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except (json.JSONDecodeError, IOError):
                self._display_boxed_menu("ERROR", ["Configuration file corrupted. Using defaults."])
                input("Press Enter to continue...")
                
        return default_config
    
    def get_default_config(self):
        """Generate platform-specific default configuration"""
        if self.platform_name == "windows":
            return {
                "project_name": "Subreal",
                "ue_version": "5.4",
                "ue_dir": "C:\\Program Files\\Epic Games\\UE_5.4",
                "project_root": str(self.script_dir),
                "editor_exe_name": "UnrealEditor.exe"
            }
        else:  # macOS
            return {
                "project_name": "Subreal", 
                "ue_version": "5.4",
                "ue_dir": "/Users/Shared/Epic Games/UE_5.4",
                "project_root": str(self.script_dir),
                "editor_exe_name": "UnrealEditor"
            }
    
    def save_config(self):
        """Save current configuration to JSON file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except IOError:
            self._display_boxed_menu("ERROR", ["Failed to save configuration."])
            input("Press Enter to continue...")
            return False
    
    def clear_screen(self):
        """Clear the console screen"""
        if self.platform_name == "windows":
            os.system('cls')
        else:
            os.system('clear')
    
    def get_key_input(self):
        """Get keyboard input for navigation"""
        if self.platform_name == "windows":
            key = msvcrt.getch()
            if key == b'\xe0':  # Arrow keys on Windows
                key = msvcrt.getch()
                if key == b'H':  # Up arrow
                    return 'UP'
                elif key == b'P':  # Down arrow
                    return 'DOWN'
                elif key == b'K':  # Left arrow
                    return 'LEFT'
                elif key == b'M':  # Right arrow
                    return 'RIGHT'
            elif key == b'\r':  # Enter
                return 'ENTER'
            elif key.lower() == b'w':
                return 'UP'
            elif key.lower() == b's':
                return 'DOWN'
            elif key.lower() == b'a':
                return 'LEFT'
            elif key.lower() == b'd':
                return 'RIGHT'
            elif key == b'\x1b':  # ESC
                return 'ESC'
        else:  # macOS/Linux
            try:
                old_settings = termios.tcgetattr(sys.stdin)
                tty.setraw(sys.stdin.fileno())
                key = sys.stdin.read(1)
                
                if key == '\x1b':  # ESC sequence
                    try:
                        key += sys.stdin.read(2)
                        if key == '\x1b[A':  # Up arrow
                            return 'UP'
                        elif key == '\x1b[B':  # Down arrow
                            return 'DOWN'
                        elif key == '\x1b[C':  # Right arrow
                            return 'RIGHT'
                        elif key == '\x1b[D':  # Left arrow
                            return 'LEFT'
                    except:
                        pass
                    return 'ESC'
                elif key == '\r' or key == '\n':
                    return 'ENTER'
                elif key.lower() == 'w':
                    return 'UP'
                elif key.lower() == 's':
                    return 'DOWN'
                elif key.lower() == 'a':
                    return 'LEFT'
                elif key.lower() == 'd':
                    return 'RIGHT'
                
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            except:
                return None
        return None
    
    def add_to_history(self, menu_name, selection=0):
        """Add current menu to navigation history"""
        if self.current_menu != menu_name:
            # Remove any forward history when navigating to a new page
            if self.history_index < len(self.navigation_history) - 1:
                self.navigation_history = self.navigation_history[:self.history_index + 1]
            
            # Add new page to history
            self.navigation_history.append({
                'menu': menu_name,
                'selection': selection
            })
            self.history_index = len(self.navigation_history) - 1
            self.current_menu = menu_name
    
    def go_back(self):
        """Navigate to previous page in history"""
        if self.history_index > 0:
            self.history_index -= 1
            return self.navigation_history[self.history_index]
        return None
    
    def go_forward(self):
        """Navigate to next page in history"""
        if self.history_index < len(self.navigation_history) - 1:
            self.history_index += 1
            return self.navigation_history[self.history_index]
        return None
    
    def can_go_back(self):
        """Check if we can go back in history"""
        return self.history_index > 0
    
    def can_go_forward(self):
        """Check if we can go forward in history"""
        return self.history_index < len(self.navigation_history) - 1
    
    def get_ascii_icons(self):
        """Get ASCII icons for menu options"""
        return {
            'build': '[#]',
            'editor': '[>]',
            'project': '[+]',
            'settings': '[*]',
            'config': '[=]',
            'exit': '[X]',
            'info': '[i]',
            'validate': '[?]',
            'directory': '[D]',
            'back': '[<]',
            'show': '[!]',
            'update': '[^]',
            'change': '[~]'
        }

    def _display_progress_bar(self, duration, prefix='', suffix='', length=50):
        """Displays a simulated progress bar for a given duration."""
        start_time = time.time()
        while True:
            elapsed = time.time() - start_time
            if elapsed > duration:
                elapsed = duration
            
            percent = (elapsed / duration)
            filled_length = int(length * percent)
            bar = bright_orange('█' * filled_length) + orange('-' * (length - filled_length))
            
            sys.stdout.write(f'\r{prefix} |{bar}| {percent:.0%} {suffix}')
            sys.stdout.flush()
            
            if elapsed == duration:
                print()
                break
            
            time.sleep(0.1)

    def _display_boxed_menu(self, title, content_lines=None, options=None, current_selection=None):
        self.clear_screen()
        self.show_banner()
        
        width = 71
        border_top = bright_orange("╭" + "─" * (width - 2) + "╮")
        border_bottom = bright_orange("╰" + "─" * (width - 2) + "╯")
        
        print(f"\n{border_top}")
        
        title_colored = bold(bright_orange(title))
        title_line = f"│{title_colored.center(width - 2 + len(title_colored) - len(title))}│"
        print(title_line)
        
        if content_lines:
            print(bright_orange("├" + "─" * (width - 2) + "┤"))
            for line in content_lines:
                colored_line = orange(line)
                visible_length = len(line)
                padding = " " * (width - visible_length - 4)
                print(f"│ {colored_line}{padding} │")
        
        if options:
            print(bright_orange("├" + "─" * (width - 2) + "┤"))
            for i, option in enumerate(options):
                if i == current_selection:
                    pointer = bright_orange(pointer_icon())
                    option_colored = bold(bright_white(option))
                    line = f"│ {pointer} {option_colored}"
                    visible_length = len(f"|  {option}")
                    padding = " " * (width - visible_length - 2)
                    print(f"{line}{padding} │")
                else:
                    option_colored = orange(option)
                    line = f"│   {option_colored}"
                    visible_length = len(f"|   {option}")
                    padding = " " * (width - visible_length - 2)
                    print(f"{line}{padding} │")

        print(border_bottom)

    def display_menu_with_selection(self, title, options, current_selection):
        """Display menu with highlighted selection, colors, and beautiful theme"""
        self._display_boxed_menu(title, options=options, current_selection=current_selection)
        
        # Navigation info with history indicators
        nav_info = self._get_navigation_info()
        nav_colored = dark_orange(nav_info)
        nav_line = f"│ {nav_colored}"
        visible_nav_length = len(f"| {nav_info}")
        nav_padding = " " * (71 - visible_nav_length - 2)
        print(f"{nav_line}{nav_padding} │")
        print(bright_orange("╰" + "─"*69 + "╯"))
    
    def _get_navigation_info(self):
        """Get navigation information with back/forward indicators"""
        nav_parts = []
        nav_parts.append("↑↓WS=Move | Enter=Select | ESC=Back")
        
        if self.can_go_back():
            nav_parts.append(f"| {back_icon()}←=Back")
        if self.can_go_forward():
            nav_parts.append(f"| {forward_icon()}→=Forward")
            
        return " ".join(nav_parts)[:50]  # Truncate if too long
    
    def show_banner(self):
        """Display welcome banner with clean Subreal ASCII art"""
        # Clean orange themed banner
        border = bright_orange("╭" + "─"*71 + "╮")
        
        print(f"\n{border}")
        print(f"{bright_orange('│')}                                                                       {bright_orange('│')}")
        
        # Clean Subreal ASCII art in orange
        subreal_lines = [
            "███████╗ ██╗   ██╗ ██████╗  ██████╗  ███████╗  █████╗  ██╗     ",
            "██╔════╝ ██║   ██║ ██╔══██╗ ██╔══██╗ ██╔════╝ ██╔══██╗ ██║     ",
            "███████╗ ██║   ██║ ██████╔╝ ██████╔╝ █████╗   ███████║ ██║     ",
            "╚════██║ ██║   ██║ ██╔══██╗ ██╔══██╗ ██╔══╝   ██╔══██║ ██║     ",
            "███████║ ╚██████╔╝ ██║  ██║ ██║  ██║ ███████╗ ██║  ██║ ███████╗",
            "╚══════╝  ╚═════╝  ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚══════╝ ╚═╝  ╚═╝ ╚══════╝"
        ]
        
        for line in subreal_lines:
            # Center each line and apply consistent orange color
            colored_line = bold(bright_orange(line))
            padding = (71 - len(line)) // 2  # Center in 71-char width
            print(f"{bright_orange('│')}{' ' * padding}{colored_line}{' ' * (71 - len(line) - padding)}{bright_orange('│')}")
        
        print(f"{bright_orange('│')}                                                                       {bright_orange('│')}")
        
        # Version info with consistent orange icons
        editor_icon_colored = orange(editor_icon())
        build_icon_colored = orange(build_icon())
        
        version_text = f"{editor_icon_colored} {bold(bright_white('Console GUI Manager v1.0'))} {editor_icon_colored}"
        version_padding = (71 - len(f"{editor_icon()} Console GUI Manager v1.0 {editor_icon()}")) // 2
        print(f"{bright_orange('│')}{' ' * version_padding}{version_text}{' ' * (71 - len(f'{editor_icon()} Console GUI Manager v1.0 {editor_icon()}') - version_padding)}{bright_orange('│')}")
        
        setup_text = f"{build_icon_colored} {bold(orange('IDE-Free Unreal Engine Development Setup'))} {build_icon_colored}"
        setup_padding = (71 - len(f"{build_icon()} IDE-Free Unreal Engine Development Setup {build_icon()}")) // 2
        print(f"{bright_orange('│')}{' ' * setup_padding}{setup_text}{' ' * (71 - len(f'{build_icon()} IDE-Free Unreal Engine Development Setup {build_icon()}') - setup_padding)}{bright_orange('│')}")
        
        print(f"{bright_orange('│')}                                                                       {bright_orange('│')}")
        print(bright_orange("╰" + "─"*71 + "╯"))
    
    def get_paths(self):
        """Get calculated paths based on configuration"""
        project_dir = Path(self.config["project_root"]) / self.config["project_name"]
        uproject_path = project_dir / f"{self.config['project_name']}.uproject"
        
        if self.platform_name == "windows":
            editor_exe = Path(self.config["ue_dir"]) / "Engine" / "Binaries" / "Win64" / self.config["editor_exe_name"]
            build_bat = Path(self.config["ue_dir"]) / "Engine" / "Build" / "BatchFiles" / "Build.bat"
            return {
                "project_dir": project_dir,
                "uproject_path": uproject_path,
                "editor_exe": editor_exe,
                "build_tool": build_bat
            }
        else:  # macOS
            editor_exe = Path(self.config["ue_dir"]) / "Engine" / "Binaries" / "Mac" / self.config["editor_exe_name"]
            build_script = Path(self.config["ue_dir"]) / "Engine" / "Build" / "BatchFiles" / "Mac" / "Build.sh"
            return {
                "project_dir": project_dir,
                "uproject_path": uproject_path,
                "editor_exe": editor_exe,
                "build_tool": build_script
            }
    
    def validate_paths(self):
        """Validate that configured paths exist"""
        paths = self.get_paths()
        issues = []
        
        if not Path(self.config["ue_dir"]).exists():
            issues.append(f"Unreal Engine directory not found: {self.config['ue_dir']}")
            
        if not paths["uproject_path"].exists():
            issues.append(f"Project file not found: {paths['uproject_path']}")
            
        if not paths["editor_exe"].exists():
            issues.append(f"Editor executable not found: {paths['editor_exe']}")
            
        if not paths["build_tool"].exists():
            issues.append(f"Build tool not found: {paths['build_tool']}")
            
        return issues
    
    def initial_setup(self):
        """Handle first-time setup or configuration choice"""
        options = [
            "Use default configuration",
            "Customize configuration"
        ]
        
        self.current_selection = 0
        
        while True:
            self._display_boxed_menu("INITIAL SETUP", content_lines=["Welcome to Subreal Engine Console GUI!"], options=options, current_selection=self.current_selection)
            
            key = self.get_key_input()
            if key == 'UP' and self.current_selection > 0:
                self.current_selection -= 1
            elif key == 'DOWN' and self.current_selection < len(options) - 1:
                self.current_selection += 1
            elif key == 'ENTER':
                if self.current_selection == 0:  # Use default
                    issues = self.validate_paths()
                    if issues:
                        content = ["Issues found with default configuration:"] + issues
                        self._display_boxed_menu("CONFIGURATION ISSUES", content_lines=content)
                        input("Press Enter to continue...")
                        self.customize_config()
                    else:
                        self._display_boxed_menu("CONFIGURATION VALIDATED", content_lines=["Default configuration validated successfully!"])
                        input("Press Enter to continue...")
                    break
                elif self.current_selection == 1:  # Customize
                    self.customize_config()
                    break
    
    def customize_config(self):
        """Interactive configuration customization"""
        self._display_boxed_menu("CONFIGURATION SETUP", content_lines=["Enter new values or press Enter to keep current."])
        
        # Project Name
        current = self.config["project_name"]
        new_name = input(f"Project name [{current}]: ").strip()
        if new_name:
            self.config["project_name"] = new_name
            
        # Unreal Engine Directory
        current = self.config["ue_dir"]
        print(f"\nCurrent Unreal Engine directory: {current}")
        new_dir = input("New UE directory (or press Enter to keep current): ").strip()
        if new_dir:
            if Path(new_dir).exists():
                self.config["ue_dir"] = new_dir
                print("[✓] Directory validated.")
            else:
                print("[!] Directory not found, but saved anyway.")
                self.config["ue_dir"] = new_dir
                
        # UE Version
        current = self.config["ue_version"]
        new_version = input(f"Unreal Engine version [{current}]: ").strip()
        if new_version:
            self.config["ue_version"] = new_version
            
        # Project Root
        current = self.config["project_root"]
        print(f"\nCurrent project root: {current}")
        new_root = input("New project root (or press Enter to keep current): ").strip()
        if new_root:
            if Path(new_root).exists():
                self.config["project_root"] = new_root
                print("[✓] Directory validated.")
            else:
                print("[!] Directory not found, but saved anyway.")
                self.config["project_root"] = new_root
        
        if self.save_config():
            self._display_boxed_menu("SUCCESS", ["Configuration saved successfully!"])
        else:
            self._display_boxed_menu("ERROR", ["Failed to save configuration."])
        input("Press Enter to continue...")
    
    def show_main_menu(self):
        """Display main menu with beautiful icons and browser-like navigation"""
        self.add_to_history("main_menu", self.current_selection)
        
        options = [
            f"{build_icon()} Build Project",
            f"{editor_icon()} Launch Editor",
            f"{project_icon()} Project Management", 
            f"{settings_icon()} Engine Settings",
            f"{config_icon()} Path Configuration",
            f"{exit_icon()} Exit"
        ]
        
        while True:
            self.display_menu_with_selection("MAIN MENU", options, self.current_selection)
            
            key = self.get_key_input()
            if key == 'UP' and self.current_selection > 0:
                self.current_selection -= 1
            elif key == 'DOWN' and self.current_selection < len(options) - 1:
                self.current_selection += 1
            elif key == 'LEFT':
                history_entry = self.go_back()
                if history_entry:
                    if history_entry['menu'] == 'main_menu':
                        self.current_selection = history_entry['selection']
                    else:
                        return self._navigate_to_menu(history_entry['menu'], history_entry['selection'])
            elif key == 'RIGHT':
                history_entry = self.go_forward()
                if history_entry:
                    if history_entry['menu'] == 'main_menu':
                        self.current_selection = history_entry['selection']
                    else:
                        return self._navigate_to_menu(history_entry['menu'], history_entry['selection'])
            elif key == 'ENTER':
                return self.current_selection + 1
            elif key == 'ESC':
                return 6  # Exit
    
    def _navigate_to_menu(self, menu_name, selection=0):
        """Navigate to a specific menu programmatically"""
        if menu_name == "project_management":
            return "project_management"
        elif menu_name == "engine_settings":
            return "engine_settings"
        return None
    
    def build_project(self):
        """Build the Unreal project using integrated build functionality"""
        self._display_boxed_menu("BUILD PROJECT", content_lines=["Building project...", "Please wait..."])
        self._display_progress_bar(2, prefix='Preparing', suffix='Complete')
        
        # Integrated functionality from build.bat
        paths = self.get_paths()
        project_name = self.config["project_name"]
        
        # Build command construction (replaces vars.bat + build.bat functionality)
        if self.platform_name == "windows":
            build_tool = Path(self.config["ue_dir"]) / "Engine" / "Build" / "BatchFiles" / "Build.bat"
            cmd = [
                str(build_tool), 
                f"{project_name}Editor", 
                "Win64", 
                "Development", 
                str(paths["uproject_path"]), 
                "-waitmutex", 
                "-NoHotReload"
            ]
        else:  # macOS
            build_tool = Path(self.config["ue_dir"]) / "Engine" / "Build" / "BatchFiles" / "Mac" / "Build.sh"
            cmd = [
                "bash", 
                str(build_tool), 
                f"{project_name}Editor", 
                "Mac", 
                "Development", 
                str(paths["uproject_path"]), 
                "-waitmutex", 
                "-NoHotReload"
            ]
        
        # Validate build tool exists
        if not Path(cmd[0] if self.platform_name != "windows" else cmd[0]).exists():
            self._display_boxed_menu("ERROR", ["Build tool not found. Check UE installation path.", f"Expected: {cmd[0]}"])
            input("Press Enter to continue...")
            return
            
        try:
            # Show actual building progress
            self._display_progress_bar(8, prefix='Building', suffix='Complete')
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                self._display_boxed_menu("SUCCESS", ["Build completed successfully!", f"Project: {project_name}", f"Platform: {self.platform_name.title()}"])
            else:
                error_lines = result.stderr.split('\n')[:5] if result.stderr else ["Unknown build error"]
                self._display_boxed_menu("BUILD FAILED", ["Build failed with errors:", ""] + [line.strip() for line in error_lines if line.strip()])
        except subprocess.TimeoutExpired:
            self._display_boxed_menu("ERROR", ["Build timed out after 10 minutes.", "Try building smaller portions or check system resources."])
        except FileNotFoundError:
            self._display_boxed_menu("ERROR", ["Build tool executable not found.", "Verify Unreal Engine installation path."])
        except Exception as e:
            self._display_boxed_menu("ERROR", [f"Unexpected build error: {str(e)[:50]}"])
        
        input("Press Enter to continue...")
    
    def launch_editor(self):
        """Launch Unreal Editor using integrated functionality"""
        self._display_boxed_menu("LAUNCH EDITOR", content_lines=["Launching Unreal Editor...", "Please wait..."])
        
        # Integrated functionality from vars.bat + editor.bat
        project_name = self.config["project_name"]
        ue_dir = Path(self.config["ue_dir"])
        project_dir = Path(self.config["project_root"]) / project_name
        uproject_path = project_dir / f"{project_name}.uproject"
        
        # Build editor executable path (replaces vars.bat functionality)
        if self.platform_name == "windows":
            editor_exe = ue_dir / "Engine" / "Binaries" / "Win64" / self.config["editor_exe_name"]
        else:  # macOS
            editor_exe = ue_dir / "Engine" / "Binaries" / "Mac" / self.config["editor_exe_name"]
        
        # Validate paths exist
        if not editor_exe.exists():
            self._display_boxed_menu("ERROR", ["Editor executable not found.", f"Expected: {editor_exe}", "Check Unreal Engine installation path."])
            input("Press Enter to continue...")
            return
            
        if not uproject_path.exists():
            self._display_boxed_menu("ERROR", ["Project file not found.", f"Expected: {uproject_path}", "Check project name and root path."])
            input("Press Enter to continue...")
            return
        
        # Launch command (replaces editor.bat functionality)
        cmd = [str(editor_exe), str(uproject_path)]
        
        try:
            self._display_progress_bar(3, prefix='Starting', suffix='Complete')
            
            if self.platform_name == "windows":
                # Launch in new console window (equivalent to 'start' in batch)
                subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:  # macOS
                subprocess.Popen(cmd)
                
            self._display_boxed_menu("SUCCESS", ["Editor launched successfully!", f"Project: {project_name}", f"Editor: {editor_exe.name}", "Check for editor window on your desktop."])
        except FileNotFoundError:
            self._display_boxed_menu("ERROR", ["Failed to start editor process.", "Verify Unreal Engine installation."])
        except PermissionError:
            self._display_boxed_menu("ERROR", ["Permission denied launching editor.", "Run as administrator or check file permissions."])
        except Exception as e:
            self._display_boxed_menu("ERROR", [f"Unexpected launch error: {str(e)[:50]}"])
            
        input("Press Enter to continue...")
    
    def project_management(self):
        """Project management submenu with browser-like navigation"""
        self.add_to_history("project_management", self.current_selection)
        options = [
            f"{icons.get_icon('info')} Show Project Info",
            f"{icons.get_icon('validate')} Validate Paths", 
            f"{icons.get_icon('directory')} Open Project Directory",
            f"{icons.get_icon('change')} Rename Project",
            f"{clean_icon()} Clean Project Files",
            f"{back_icon()} Back to Main Menu"
        ]
        while True:
            self._display_boxed_menu("PROJECT MANAGEMENT", options=options, current_selection=self.current_selection)
            key = self.get_key_input()
            if key == 'UP' and self.current_selection > 0:
                self.current_selection -= 1
            elif key == 'DOWN' and self.current_selection < len(options) - 1:
                self.current_selection += 1
            elif key == 'ENTER':
                if self.current_selection == 0:
                    self.show_project_info()
                elif self.current_selection == 1:
                    self.validate_and_show_paths()
                elif self.current_selection == 2:
                    self.open_project_directory()
                elif self.current_selection == 3:
                    self.rename_project()
                elif self.current_selection == 4:
                    self.clean_project_files()
                elif self.current_selection == 5:
                    break
            elif key == 'ESC':
                break
    
    def show_project_info(self):
        """Display current project information with colors"""
        paths = self.get_paths()
        content = [
            f"Project Name: {self.config['project_name']}",
            f"UE Version: {self.config['ue_version']}",
            f"Platform: {self.platform_name.title()}",
            f"Project Dir: {paths['project_dir']}"
        ]
        self._display_boxed_menu("PROJECT INFORMATION", content_lines=content)
        input("Press Enter to continue...")
    
    def validate_and_show_paths(self):
        """Validate and display path status"""
        issues = self.validate_paths()
        if not issues:
            self._display_boxed_menu("PATH VALIDATION", ["All paths are valid!"])
        else:
            self._display_boxed_menu("PATH VALIDATION", ["Path validation issues found:"] + issues)
        input("Press Enter to continue...")
    
    def open_project_directory(self):
        """Open project directory in file explorer"""
        paths = self.get_paths()
        try:
            if self.platform_name == "windows":
                subprocess.run(["explorer", str(paths["project_dir"])])
            else:  # macOS
                subprocess.run(["open", str(paths["project_dir"])])
            self._display_boxed_menu("SUCCESS", ["Project directory opened!"])
        except Exception as e:
            self._display_boxed_menu("ERROR", [f"Could not open directory: {e}"])
        input("Press Enter to continue...")
    
    def rename_project(self):
        """Rename project with comprehensive validation and safety checks"""
        try:
            # Initialize renamer
            renamer = ProjectRenamer(self.config["project_root"], self.config["project_name"])
            
            # Step 1: Detect project type
            self._display_boxed_menu("ANALYZING PROJECT", ["Detecting project type...", "Please wait..."])
            self._display_progress_bar(2, prefix='Scanning', suffix='Complete')
            
            project_info = renamer.detect_project_type()
            
            if 'error' in project_info:
                self._display_boxed_menu("ERROR", [project_info['error']])
                input("Press Enter to continue...")
                return
            
            # Step 2: Show project analysis
            self._show_project_analysis(project_info)
            
            # Step 3: Get new name from user
            new_name = self._get_new_project_name()
            if not new_name:
                return  # User cancelled
            
            # Step 4: Validate new name
            validation = renamer.validate_new_name(new_name)
            if not validation['valid']:
                self._display_boxed_menu("INVALID PROJECT NAME", validation['errors'])
                input("Press Enter to continue...")
                return
            
            # Step 5: Show warnings and get confirmation
            if not self._confirm_project_rename(new_name, project_info, validation):
                return  # User cancelled
            
            # Step 6: Create backup and perform rename
            self._perform_project_rename(renamer, new_name, project_info)
            
        except Exception as e:
            self._display_boxed_menu("UNEXPECTED ERROR", [f"Project rename failed: {str(e)[:60]}"])
            input("Press Enter to continue...")
    
    def _show_project_analysis(self, project_info):
        """Display project type analysis"""
        content = [
            f"Project Type: {project_info['type'].upper()}",
            f"Has Source Code: {'Yes' if project_info['has_source'] else 'No'}",
            f"Has Binaries: {'Yes' if project_info['has_binaries'] else 'No'}"
        ]
        
        if project_info['type'] == 'cpp':
            content.append(f"C++ Modules: {len(project_info['modules'])}")
            content.append(f"Source Files: {len(project_info['source_files'])}")
            content.append("")
            content.append(f"{warning_icon()} C++ projects require additional steps")
        else:
            content.append("")
            content.append(f"{success_icon()} Blueprint-only project (simpler rename)")
        
        if 'warning' in project_info:
            content.append(f"{warning_icon()} {project_info['warning']}")
        
        self._display_boxed_menu("PROJECT ANALYSIS", content_lines=content)
        input("Press Enter to continue...")
    
    def _get_new_project_name(self) -> str:
        """Get new project name from user"""
        self._display_boxed_menu("ENTER NEW PROJECT NAME", [
            f"Current project: {self.config['project_name']}",
            "",
            "Enter new project name:",
            "• Leave empty to cancel",
            "• Avoid spaces and special characters",
            "• Use CamelCase or underscore_case"
        ])
        
        new_name = input("New project name: ").strip()
        return new_name if new_name else None
    
    def _confirm_project_rename(self, new_name: str, project_info: Dict, validation: Dict) -> bool:
        """Show confirmation dialog with warnings"""
        content = [
            f"Rename '{self.config['project_name']}' to '{new_name}'",
            "",
            f"{warning_icon()} WARNING: This action cannot be undone!",
            f"{warning_icon()} Complex projects may have issues!",
            ""
        ]
        
        if project_info['type'] == 'cpp':
            content.extend([
                f"C++ Project Changes:",
                f"• Rename source files and directories",
                f"• Update #include statements", 
                f"• Update module references",
                f"• Add redirect entries",
                f"• Clean generated files",
                ""
            ])
        else:
            content.extend([
                f"Blueprint Project Changes:",
                f"• Rename .uproject file",
                f"• Update configuration files",
                f"• Rename project directory",
                ""
            ])
        
        if validation['warnings']:
            content.append("Warnings:")
            for warning in validation['warnings']:
                content.append(f"• {warning}")
            content.append("")
        
        content.extend([
            "A backup will be created before renaming.",
            "",
            f"{success_icon()} Proceed with rename?",
            f"{error_icon()} Cancel operation?"
        ])
        
        options = [
            f"{success_icon()} Yes, Rename Project",
            f"{error_icon()} No, Cancel"
        ]
        
        current_selection = 0
        while True:
            self._display_boxed_menu("CONFIRM PROJECT RENAME", content_lines=content, options=options, current_selection=current_selection)
            key = self.get_key_input()
            if key == 'UP' and current_selection > 0:
                current_selection -= 1
            elif key == 'DOWN' and current_selection < len(options) - 1:
                current_selection += 1
            elif key == 'ENTER':
                return current_selection == 0
            elif key == 'ESC':
                return False
    
    def _perform_project_rename(self, renamer: ProjectRenamer, new_name: str, project_info: Dict):
        """Perform the actual project rename with progress tracking"""
        try:
            # Create backup
            self._display_boxed_menu("CREATING BACKUP", ["Creating project backup...", "Please wait..."])
            self._display_progress_bar(3, prefix='Backing up', suffix='Complete')
            
            backup_path = renamer.create_backup()
            
            # Rename files and update content
            self._display_boxed_menu("RENAMING PROJECT", ["Updating project files...", "Please wait..."])
            self._display_progress_bar(5, prefix='Renaming', suffix='Complete')
            
            rename_result = renamer.rename_project_files(new_name)
            
            # Rename project directory
            self._display_boxed_menu("FINALIZING", ["Renaming project directory...", "Please wait..."])
            self._display_progress_bar(2, prefix='Finalizing', suffix='Complete')
            
            if renamer.rename_project_directory(new_name):
                # Update configuration
                self.config["project_name"] = new_name
                self.save_config()
                
                # Show success
                success_content = [
                    f"✅ Project successfully renamed!",
                    f"Old name: {renamer.current_name}",
                    f"New name: {new_name}",
                    f"Backup created: {Path(backup_path).name}",
                    "",
                    "Changes made:"
                ]
                
                for change in rename_result['changes'][:10]:  # Show first 10 changes
                    success_content.append(f"• {change}")
                
                if len(rename_result['changes']) > 10:
                    success_content.append(f"... and {len(rename_result['changes']) - 10} more changes")
                
                if rename_result['errors']:
                    success_content.append("")
                    success_content.append("⚠️ Some issues occurred:")
                    for error in rename_result['errors'][:3]:
                        success_content.append(f"• {error}")
                
                if project_info['type'] == 'cpp':
                    success_content.extend([
                        "",
                        "📝 Next steps for C++ projects:",
                        "• Right-click .uproject → Generate VS files",
                        "• Recompile your project",
                        "• Test all Blueprint references"
                    ])
                
                self._display_boxed_menu("RENAME SUCCESSFUL", content_lines=success_content)
            else:
                # Directory rename failed
                self._display_boxed_menu("ERROR", [
                    "Failed to rename project directory.",
                    "Files have been updated but directory rename failed.",
                    "You may need to rename manually or restore from backup."
                ])
                
        except Exception as e:
            # Show rollback option
            self._handle_rename_failure(renamer, str(e))
        
        input("Press Enter to continue...")
    
    def _handle_rename_failure(self, renamer: ProjectRenamer, error: str):
        """Handle rename failure with rollback option"""
        content = [
            "Project rename failed!",
            f"Error: {error[:50]}",
            "",
            "Would you like to restore from backup?"
        ]
        
        options = [
            f"{success_icon()} Yes, Restore Backup",
            f"{error_icon()} No, Keep Changes"
        ]
        
        current_selection = 0
        while True:
            self._display_boxed_menu("RENAME FAILED", content_lines=content, options=options, current_selection=current_selection)
            key = self.get_key_input()
            if key == 'UP' and current_selection > 0:
                current_selection -= 1
            elif key == 'DOWN' and current_selection < len(options) - 1:
                current_selection += 1
            elif key == 'ENTER':
                if current_selection == 0:
                    # Attempt rollback
                    self._display_boxed_menu("RESTORING BACKUP", ["Restoring project from backup..."])
                    self._display_progress_bar(3, prefix='Restoring', suffix='Complete')
                    
                    if renamer.rollback_changes():
                        self._display_boxed_menu("SUCCESS", ["Project restored from backup successfully!"])
                    else:
                        self._display_boxed_menu("ERROR", ["Failed to restore from backup.", "Manual recovery may be needed."])
                break
            elif key == 'ESC':
                break
    
    def clean_project_files(self):
        """Clean non-essential project files with preview and confirmation"""
        try:
            paths = self.get_paths()
            project_dir = paths['project_dir']
            if not project_dir.exists():
                self._display_boxed_menu("ERROR", [f"Project directory not found: {project_dir}"])
                return
            
            cleaner = ProjectCleaner(str(project_dir))
            self._display_boxed_menu("SCANNING PROJECT", ["Scanning project for cleanup candidates...", "Please wait..."])
            self._display_progress_bar(2, prefix='Scanning', suffix='Complete')
            scan_results = cleaner.scan_project()
            
            cleanup_options = self._show_cleanup_preview(cleaner, scan_results)
            if cleanup_options:
                self._perform_cleanup(cleaner, scan_results, cleanup_options)
        except Exception as e:
            self._display_boxed_menu("ERROR", [f"An error occurred during cleanup: {str(e)}"])
    
    def _show_cleanup_preview(self, cleaner: ProjectCleaner, scan_results: dict) -> dict:
        """Show cleanup preview with button-style navigation"""
        total_files = sum(data['count'] for data in scan_results.values() if data['files'])
        total_size = sum(data['total_size'] for data in scan_results.values() if data['files'])
        title = f"PROJECT CLEANUP PREVIEW - {total_files} FILES ({cleaner.format_size(total_size)})"
        
        content = []
        for category, data in scan_results.items():
            if data['files']:
                icon = clean_icon() if cleaner.is_safe_to_delete(category) else warning_icon()
                desc = cleaner.get_category_description(category)
                count = data['count']
                size_str = cleaner.format_size(data['total_size'])
                content.append(f"{icon} {desc:<35} | {count:>5} items | {size_str:>10}")

        options = [
            f"{clean_icon()} Proceed with Cleanup",
            f"{icons.get_icon('info')} Show Detailed File List",
            f"{back_icon()} Cancel Cleanup"
        ]
        
        current_selection = 0
        while True:
            self._display_boxed_menu(title, content_lines=content, options=options, current_selection=current_selection)
            key = self.get_key_input()
            if key == 'UP' and current_selection > 0:
                current_selection -= 1
            elif key == 'DOWN' and current_selection < len(options) - 1:
                current_selection += 1
            elif key == 'ENTER':
                if current_selection == 0:
                    return self._get_cleanup_options(cleaner, scan_results)
                elif current_selection == 1:
                    self._show_detailed_preview(cleaner, scan_results)
                    continue
                elif current_selection == 2:
                    return None
            elif key == 'ESC':
                return None

    def _get_cleanup_options(self, cleaner: ProjectCleaner, scan_results: dict) -> dict:
        """Get user options for backup and cleanup preferences"""
        options = [
            f"{icons.get_icon('save')} Create Backup List",
            f"{clean_icon()} Skip Backup (Save Space)",
            f"{back_icon()} Cancel Cleanup"
        ]
        
        current_selection = 0
        while True:
            self._display_boxed_menu("BACKUP OPTIONS", content_lines=["Backup list records what files will be deleted", "Useful for recovery if needed later", f"{warning_icon()} Skipping backup saves disk space but no recovery"], options=options, current_selection=current_selection)
            key = self.get_key_input()
            if key == 'UP' and current_selection > 0:
                current_selection -= 1
            elif key == 'DOWN' and current_selection < len(options) - 1:
                current_selection += 1
            elif key == 'ENTER':
                if current_selection == 0:
                    return {'create_backup': True, 'proceed': True}
                elif current_selection == 1:
                    return {'create_backup': False, 'proceed': True}
                elif current_selection == 2:
                    return None
            elif key == 'ESC':
                return None

    def _show_detailed_preview(self, cleaner: ProjectCleaner, scan_results: dict):
        """Show detailed file list for review"""
        content = []
        for category, data in scan_results.items():
            if data['files']:
                content.append(f"{bright_orange(cleaner.get_category_description(category))}:")
                content.append('-' * 62)
                for file_data in data['files'][:10]:
                    file_path = str(file_data['path'].relative_to(cleaner.project_root))
                    file_size = cleaner.format_size(file_data['size'])
                    if len(file_path) > 45:
                        file_path = file_path[:42] + "..."
                    content.append(f"  {orange(file_path):<45} ({bright_white(file_size)}) ")
                if len(data['files']) > 10:
                    content.append(f"  {dark_orange(f'... and {len(data['files']) - 10} more files')}")
                content.append("")
        self._display_boxed_menu("DETAILED FILE LIST", content_lines=content)
        input("Press Enter to continue...")

    def _perform_cleanup(self, cleaner: ProjectCleaner, scan_results: dict, cleanup_options: dict):
        """Perform the actual cleanup with progress indication"""
        self._display_boxed_menu("CLEANING PROJECT", ["Cleaning project...", "Please wait..."])
        
        total_deleted_files = 0
        total_deleted_size = 0
        
        if cleanup_options['create_backup']:
            backup_file = cleaner.create_backup_list(scan_results)
            self._display_boxed_menu("CLEANING PROJECT", [f"Backup list created: {Path(backup_file).name}"])
        
        for category, data in scan_results.items():
            if data['files'] and cleaner.is_safe_to_delete(category):
                self._display_progress_bar(1, prefix=f'Cleaning {cleaner.get_category_description(category)}', suffix='Complete')
                deleted_count, deleted_size = cleaner.clean_category(category, data['files'])
                total_deleted_files += deleted_count
                total_deleted_size += deleted_size
        
        empty_dirs_removed = cleaner.clean_empty_directories()
        total_items = total_deleted_files + empty_dirs_removed
        
        if total_items > 0:
            content = [
                "CLEANUP COMPLETE!",
                f"Removed {total_items} files/folders/directories",
                f"Freed up {cleaner.format_size(total_deleted_size)} of disk space"
            ]
            if cleanup_options['create_backup']:
                content.append(f"Backup list saved to: {Path(backup_file).name}")
            self._display_boxed_menu("SUCCESS", content)
        else:
            self._display_boxed_menu("INFO", ["No files were removed."])
        
        input("Press Enter to continue...")
    
    def engine_settings(self):
        """Engine settings submenu with browser-like navigation"""
        self.add_to_history("engine_settings", self.current_selection)
        options = [
            f"{icons.get_icon('show')} Show Current Settings",
            f"{icons.get_icon('update')} Update UE Version",
            f"{icons.get_icon('change')} Change UE Directory", 
            f"{back_icon()} Back to Main Menu"
        ]
        while True:
            self._display_boxed_menu("ENGINE SETTINGS", options=options, current_selection=self.current_selection)
            key = self.get_key_input()
            if key == 'UP' and self.current_selection > 0:
                self.current_selection -= 1
            elif key == 'DOWN' and self.current_selection < len(options) - 1:
                self.current_selection += 1
            elif key == 'ENTER':
                if self.current_selection == 0:
                    self.show_engine_settings()
                elif self.current_selection == 1:
                    self.update_ue_version()
                elif self.current_selection == 2:
                    self.change_ue_directory()
                elif self.current_selection == 3:
                    break
            elif key == 'ESC':
                break
    
    def show_engine_settings(self):
        """Display current engine settings"""
        paths = self.get_paths()
        content = [
            f"UE Version: {self.config['ue_version']}",
            f"UE Directory: {self.config['ue_dir']}",
            f"Editor Executable: {paths['editor_exe']}",
            f"Build Tool: {paths['build_tool']}"
        ]
        self._display_boxed_menu("ENGINE SETTINGS", content_lines=content)
        input("Press Enter to continue...")
    
    def update_ue_version(self):
        """Update Unreal Engine version"""
        self._display_boxed_menu("UPDATE UE VERSION", [f"Current version: {self.config['ue_version']}"])
        new_version = input("Enter new UE version: ").strip()
        if new_version and new_version != self.config["ue_version"]:
            self.config["ue_version"] = new_version
            if self.save_config():
                self._display_boxed_menu("SUCCESS", ["UE version updated successfully!"])
            else:
                self._display_boxed_menu("ERROR", ["Failed to save configuration."])
        else:
            self._display_boxed_menu("INFO", ["No changes made."])
        input("Press Enter to continue...")
    
    def change_ue_directory(self):
        """Change Unreal Engine directory"""
        self._display_boxed_menu("CHANGE UE DIRECTORY", [f"Current directory: {self.config['ue_dir']}"])
        new_dir = input("Enter new UE directory: ").strip()
        if new_dir:
            if Path(new_dir).exists():
                self.config["ue_dir"] = new_dir
                if self.save_config():
                    self._display_boxed_menu("SUCCESS", ["UE directory updated and validated!"])
                else:
                    self._display_boxed_menu("ERROR", ["Failed to save configuration."])
            else:
                confirm = input("[!] Directory not found. Save anyway? (y/n): ")
                if confirm.lower().startswith('y'):
                    self.config["ue_dir"] = new_dir
                    if self.save_config():
                        self._display_boxed_menu("INFO", ["UE directory updated (not validated)."])
                    else:
                        self._display_boxed_menu("ERROR", ["Failed to save configuration."])
        else:
            self._display_boxed_menu("INFO", ["No changes made."])
        input("Press Enter to continue...")
    
    def path_configuration(self):
        """Path configuration submenu - same as customize_config but as menu option"""
        self.customize_config()
    
    def run(self):
        """Main application loop"""
        if not self.config_file.exists() or not self.config:
            self.initial_setup()
        else:
            self.clear_screen()
            self.show_banner()
        
        while True:
            result = self.show_main_menu()
            
            if result == "project_management":
                self.project_management()
                continue
            elif result == "engine_settings":
                self.engine_settings() 
                continue
            
            choice = result if isinstance(result, int) else None
            if choice == 1:
                self.build_project()
            elif choice == 2:
                self.launch_editor()
            elif choice == 3:
                self.project_management()
            elif choice == 4:
                self.engine_settings()
            elif choice == 5:
                self.path_configuration()
            elif choice == 6:
                self.clear_screen()
                farewell = bold(bright_orange("Thank you for using Subreal Engine Console GUI!"))
                exit_icon_colored = orange(exit_icon())
                print(f"\n{exit_icon_colored} {farewell} {exit_icon_colored}")
                sys.exit(0)

def main():
    """Entry point - replaces launch_gui.bat functionality"""
    try:
        print(bright_orange("Starting Subreal Engine Console GUI..."))
        time.sleep(0.5)  # Brief pause for user to see startup message
        app = SubrealGUI()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{orange('👋')} {bold(bright_orange('Goodbye!'))} {orange('👋')}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{bold(bright_orange('UNEXPECTED ERROR'))}")
        print(f"{orange('Error:')} {str(e)}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
