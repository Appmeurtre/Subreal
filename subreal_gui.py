#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import platform
from pathlib import Path

# Add vendor directory to path for bundled libraries
vendor_path = Path(__file__).parent / "vendor"
if str(vendor_path) not in sys.path:
    sys.path.insert(0, str(vendor_path))

# Import bundled libraries
from colors import orange, bright_orange, dark_orange, bold, underline, bright_white, color_manager
from icons import icons, build_icon, editor_icon, project_icon, settings_icon, config_icon, exit_icon
from icons import success_icon, error_icon, warning_icon, back_icon, forward_icon, pointer_icon, clean_icon, trash_icon
from cleaner import ProjectCleaner

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
                print("⚠️  Configuration file corrupted. Using defaults.")
                
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
            print("❌ Failed to save configuration.")
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

    def display_menu_with_selection(self, title, options, current_selection):
        """Display menu with highlighted selection, colors, and beautiful theme"""
        self.clear_screen()
        self.show_banner()
        
        # Orange themed borders with color - match banner width
        border_color = bright_orange("+" + "="*66 + "+")
        print(f"\n{border_color}")
        
        # Colorful title
        title_colored = bold(bright_orange(title))
        title_line = f"|{title_colored.center(66 + len(title_colored) - len(title))}|"
        print(title_line)
        print(border_color)
        
        # Display options with beautiful icons and colors
        for i, option in enumerate(options):
            if i == current_selection:
                # Highlighted option with pointer and bright colors
                pointer = bright_orange(pointer_icon())
                option_colored = bold(bright_white(option))
                line = f"| {pointer} {option_colored}"
                # Pad to correct length accounting for color codes
                visible_length = len(f"| {pointer_icon()} {option}")
                padding = " " * (66 - visible_length)
                print(f"{line}{padding} |")
            else:
                # Regular option with muted colors
                option_colored = orange(option)
                line = f"|   {option_colored}"
                # Pad to correct length accounting for color codes
                visible_length = len(f"|   {option}")
                padding = " " * (66 - visible_length)
                print(f"{line}{padding} |")
        
        print(border_color)
        
        # Navigation info with history indicators
        nav_info = self._get_navigation_info()
        nav_colored = dark_orange(nav_info)
        nav_line = f"| {nav_colored}"
        visible_nav_length = len(f"| {nav_info}")
        nav_padding = " " * (66 - visible_nav_length)
        print(f"{nav_line}{nav_padding} |")
        print(border_color)
    
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
        """Display welcome banner with beautiful Subreal ASCII art"""
        # Orange themed banner with custom Subreal logo
        border = bright_orange("+==================================================================+")
        
        print(f"\n{border}")
        print(f"{bright_orange('|')}                                                                  {bright_orange('|')}")
        
        # Beautiful Subreal ASCII art in bright orange
        subreal_lines = [
            " ____             __                            ___      ",
            "/\\  _`\\          /\\ \\                          /\\_ \\     ",
            "\\ \\,\\L\\_\\  __  __\\ \\ \\____  _ __    __     __  \\//\\ \\    ",
            " \\/_\\__ \\ /\\ \\/\\ \\\\ \\ '__`\\/\\`'__\\/'__`\\ /'__`\\  \\ \\ \\   ",
            "   /\\ \\L\\ \\ \\ \\_\\ \\\\ \\ \\L\\ \\ \\ \\//\\  __//\\ \\L\\.\\_ \\_\\ \\_ ",
            "   \\ `\\____\\ \\____/ \\ \\_,__/\\ \\_\\\\ \\____\\ \\__/.\\_\\/\\____\\",
            "    \\/_____/\\/___/   \\/___/  \\/_/ \\/____/\\/__/\\/_/\\/____/"
        ]
        
        for line in subreal_lines:
            # Center each line and apply bright orange color
            colored_line = bold(bright_orange(line))
            padding = (66 - len(line)) // 2  # Center in 66-char width
            print(f"{bright_orange('|')}{' ' * padding}{colored_line}{' ' * (66 - len(line) - padding)}{bright_orange('|')}")
        
        print(f"{bright_orange('|')}                                                                  {bright_orange('|')}")
        
        # Version info with icons
        editor_icon_colored = bright_orange(editor_icon())
        build_icon_colored = bright_orange(build_icon())
        
        version_text = f"{editor_icon_colored} {bold(bright_white('Console GUI Manager v1.0'))} {editor_icon_colored}"
        version_padding = (66 - len(f"{editor_icon()} Console GUI Manager v1.0 {editor_icon()}")) // 2
        print(f"{bright_orange('|')}{' ' * version_padding}{version_text}{' ' * (66 - len(f'{editor_icon()} Console GUI Manager v1.0 {editor_icon()}') - version_padding)}{bright_orange('|')}")
        
        setup_text = f"{build_icon_colored} {bold(orange('IDE-Free Unreal Engine Development Setup'))} {build_icon_colored}"
        setup_padding = (66 - len(f"{build_icon()} IDE-Free Unreal Engine Development Setup {build_icon()}")) // 2
        print(f"{bright_orange('|')}{' ' * setup_padding}{setup_text}{' ' * (66 - len(f'{build_icon()} IDE-Free Unreal Engine Development Setup {build_icon()}') - setup_padding)}{bright_orange('|')}")
        
        print(f"{bright_orange('|')}                                                                  {bright_orange('|')}")
        print(border)
    
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
            self.clear_screen()
            self.show_banner()
            
            print("\nWelcome to Subreal Engine Console GUI!")
            border = bright_orange("+" + "="*66 + "+")
            print(f"\n{border}")
            
            title = bold(bright_orange("INITIAL SETUP"))
            print(f"|{title.center(66 + len(title) - len('INITIAL SETUP'))}|")
            print(border)
            
            for i, option in enumerate(options):
                if i == self.current_selection:
                    pointer = bright_orange(">>")
                    option_colored = bold(bright_white(option))
                    line = f"| {pointer} {option_colored}"
                    visible_length = len(f"| >> {option}")
                    padding = " " * (66 - visible_length)
                    print(f"{line}{padding} |")
                else:
                    option_colored = orange(option)
                    line = f"|   {option_colored}"
                    visible_length = len(f"|   {option}")
                    padding = " " * (66 - visible_length)
                    print(f"{line}{padding} |")
            
            print(border)
            nav_text = dark_orange("Navigation: ↑↓WS=Move | Enter=Select | ESC=Back")
            nav_line = f"| {nav_text}"
            nav_padding = " " * (66 - len("| Navigation: ↑↓WS=Move | Enter=Select | ESC=Back"))
            print(f"{nav_line}{nav_padding} |")
            print(border)
            
            key = self.get_key_input()
            if key == 'UP' and self.current_selection > 0:
                self.current_selection -= 1
            elif key == 'DOWN' and self.current_selection < len(options) - 1:
                self.current_selection += 1
            elif key == 'LEFT':
                # Left arrow: go to previous option
                if self.current_selection > 0:
                    self.current_selection -= 1
            elif key == 'RIGHT':
                # Right arrow: go to next option
                if self.current_selection < len(options) - 1:
                    self.current_selection += 1
            elif key == 'ENTER':
                if self.current_selection == 0:  # Use default
                    issues = self.validate_paths()
                    if issues:
                        self.clear_screen()
                        self.show_banner()
                        
                        border = "+" + "="*58 + "+"
                        print(f"\n{border}")
                        print(f"|{'CONFIGURATION ISSUES'.center(58)}|")
                        print(border)
                        print("| [!] Issues found with default configuration:            |")
                        print("|                                                          |")
                        for issue in issues:
                            truncated = issue[:54] if len(issue) <= 54 else issue[:51] + "..."
                            print(f"| * {truncated.ljust(54)} |")
                        print("|                                                          |")
                        print("| Would you like to customize the configuration instead?  |")
                        print("| Press Enter to customize, or ESC to continue defaults   |")
                        print(border)
                        
                        key = self.get_key_input()
                        if key == 'ENTER':
                            self.customize_config()
                        else:
                            print("| [!] Continuing with potentially invalid paths...        |")
                            print(border)
                            print("| Press Enter to continue...                               |")
                            print(border)
                            input()
                    else:
                        self.clear_screen()
                        self.show_banner()
                        border = "+" + "="*58 + "+"
                        print(f"\n{border}")
                        print(f"|{'CONFIGURATION VALIDATED'.center(58)}|")
                        print(border)
                        print("| [✓] Default configuration validated successfully!       |")
                        print(border)
                        print("| Press Enter to continue...                               |")
                        print(border)
                        input()
                    break
                elif self.current_selection == 1:  # Customize
                    self.customize_config()
                    break
    
    def customize_config(self):
        """Interactive configuration customization"""
        print("\n" + "="*60)
        print("           🔧 CONFIGURATION SETUP")
        print("="*60)
        
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
            print("\n[✓] Configuration saved successfully!")
        else:
            print("\n[X] Failed to save configuration.")
    
    def show_main_menu(self):
        """Display main menu with beautiful icons and browser-like navigation"""
        # Add to navigation history
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
                # Browser-like back navigation
                history_entry = self.go_back()
                if history_entry:
                    if history_entry['menu'] == 'main_menu':
                        self.current_selection = history_entry['selection']
                    else:
                        # Navigate to the historical menu
                        return self._navigate_to_menu(history_entry['menu'], history_entry['selection'])
            elif key == 'RIGHT':
                # Browser-like forward navigation
                history_entry = self.go_forward()
                if history_entry:
                    if history_entry['menu'] == 'main_menu':
                        self.current_selection = history_entry['selection']
                    else:
                        # Navigate to the historical menu
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
        # Add more menu mappings as needed
        return None
    
    def build_project(self):
        """Build the Unreal project"""
        self.clear_screen()
        self.show_banner()
        
        border = "+" + "="*58 + "+"
        print(f"\n{border}")
        print(f"|{'BUILD PROJECT'.center(58)}|")
        print(border)
        print("| [#] Building project...                                  |")
        print(border)
        paths = self.get_paths()
        
        if self.platform_name == "windows":
            cmd = [
                str(paths["build_tool"]),
                f"{self.config['project_name']}Editor",
                "Win64",
                "Development", 
                str(paths["uproject_path"]),
                "-waitmutex",
                "-NoHotReload"
            ]
        else:  # macOS
            cmd = [
                "bash",
                str(paths["build_tool"]),
                f"{self.config['project_name']}Editor",
                "Mac",
                "Development",
                str(paths["uproject_path"]),
                "-waitmutex",
                "-NoHotReload"
            ]
        
        try:
            print("| Executing build command...                               |")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("| [✓] Build completed successfully!                       |")
            else:
                print("| [X] Build failed!                                       |")
                if result.stderr:
                    print("|                                                          |")
                    print("| Error output:                                            |")
                    # Show first few lines of error, truncated to fit
                    error_lines = result.stderr.split('\n')[:5]
                    for line in error_lines:
                        truncated = line[:56] if len(line) <= 56 else line[:53] + "..."
                        if truncated.strip():
                            print(f"| {truncated.ljust(56)} |")
                    
        except subprocess.TimeoutExpired:
            print("| [!] Build timed out after 5 minutes.                    |")
        except FileNotFoundError:
            print("| [X] Build tool not found. Check configuration.          |")
        except Exception as e:
            error_msg = str(e)[:50] if len(str(e)) <= 50 else str(e)[:47] + "..."
            print(f"| [X] Build error: {error_msg.ljust(42)} |")
            
        print(border)
        print("| Press Enter to continue...                               |")
        print(border)
        input()
    
    def launch_editor(self):
        """Launch Unreal Editor"""
        self.clear_screen()
        self.show_banner()
        
        border = "+" + "="*58 + "+"
        print(f"\n{border}")
        print(f"|{'LAUNCH EDITOR'.center(58)}|")
        print(border)
        print("| [>] Launching Unreal Editor...                          |")
        
        paths = self.get_paths()
        cmd = [str(paths["editor_exe"]), str(paths["uproject_path"])]
        
        try:
            if self.platform_name == "windows":
                subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen(cmd)
            print("| [✓] Editor launched successfully!                       |")
            
        except FileNotFoundError:
            print("| [X] Editor executable not found. Check configuration.   |")
        except Exception as e:
            error_msg = str(e)[:50] if len(str(e)) <= 50 else str(e)[:47] + "..."
            print(f"| [X] Launch error: {error_msg.ljust(43)} |")
            
        print(border)
        print("| Press Enter to continue...                               |")
        print(border)
        input()
    
    def project_management(self):
        """Project management submenu with browser-like navigation"""
        # Add to navigation history
        self.add_to_history("project_management", self.current_selection)
        
        options = [
            f"{icons.get_icon('info')} Show Project Info",
            f"{icons.get_icon('validate')} Validate Paths", 
            f"{icons.get_icon('directory')} Open Project Directory",
            f"{clean_icon()} Clean Project Files",
            f"{back_icon()} Back to Main Menu"
        ]
        
        while True:
            self.display_menu_with_selection("PROJECT MANAGEMENT", options, self.current_selection)
            
            key = self.get_key_input()
            choice = None
            
            if key == 'UP' and self.current_selection > 0:
                self.current_selection -= 1
            elif key == 'DOWN' and self.current_selection < len(options) - 1:
                self.current_selection += 1
            elif key == 'LEFT':
                # Browser-like back navigation
                history_entry = self.go_back()
                if history_entry:
                    if history_entry['menu'] == 'main_menu':
                        return  # Go back to main menu
                    elif history_entry['menu'] == 'project_management':
                        self.current_selection = history_entry['selection']
            elif key == 'RIGHT':
                # Browser-like forward navigation
                history_entry = self.go_forward()
                if history_entry:
                    if history_entry['menu'] == 'project_management':
                        self.current_selection = history_entry['selection']
            elif key == 'ENTER':
                choice = self.current_selection + 1
            elif key == 'ESC':
                break
                
            if choice == 1:
                self.show_project_info()
            elif choice == 2:
                self.validate_and_show_paths()
            elif choice == 3:
                self.open_project_directory()
            elif choice == 4:
                self.clean_project_files()
            elif choice == 5:
                break
    
    def show_project_info(self):
        """Display current project information with colors"""
        self.clear_screen()
        self.show_banner()
        paths = self.get_paths()
        
        border = bright_orange("+" + "="*66 + "+")
        print(f"\n{border}")
        
        title = bold(bright_orange("PROJECT INFORMATION"))
        print(f"|{title.center(66 + len(title) - len('PROJECT INFORMATION'))}|")
        print(border)
        
        # Colorful project information
        info_icon = bright_orange(icons.get_icon('info'))
        project_name = bold(bright_white(self.config['project_name'][:40]))
        ue_version = orange(self.config['ue_version'][:42])
        platform_name = orange(self.platform_name.title()[:44])
        
        print(f"| {info_icon} Project Name: {project_name.ljust(48 + len(project_name) - len(self.config['project_name'][:40]))} |")
        print(f"| {info_icon} UE Version: {ue_version.ljust(50 + len(ue_version) - len(self.config['ue_version'][:42]))} |")
        print(f"| {info_icon} Platform: {platform_name.ljust(52 + len(platform_name) - len(self.platform_name.title()[:44]))} |")
        
        dir_str = str(paths['project_dir'])[:58]
        project_dir = dark_orange(dir_str)
        print(f"| {info_icon} Project Dir: {project_dir.ljust(58 + len(project_dir) - len(dir_str))} |")
        
        print(border)
        continue_msg = dark_orange("Press Enter to continue...")
        print(f"| {continue_msg.ljust(66 + len(continue_msg) - len('Press Enter to continue...'))} |")
        print(border)
        input()
    
    def validate_and_show_paths(self):
        """Validate and display path status"""
        self.clear_screen()
        self.show_banner()
        
        border = "+" + "="*58 + "+"
        print(f"\n{border}")
        print(f"|{'PATH VALIDATION'.center(58)}|")
        print(border)
        
        issues = self.validate_paths()
        
        if not issues:
            print("| [✓] All paths are valid!                                 |")
        else:
            print("| [!] Path validation issues found:                       |")
            print("|                                                          |")
            for issue in issues:
                # Truncate long paths to fit in the box
                truncated = issue[:54] if len(issue) <= 54 else issue[:51] + "..."
                print(f"| * {truncated.ljust(54)} |")
        
        print(border)
        print("| Press Enter to continue...                               |")
        print(border)
        input()
    
    def open_project_directory(self):
        """Open project directory in file explorer"""
        self.clear_screen()
        self.show_banner()
        paths = self.get_paths()
        
        try:
            if self.platform_name == "windows":
                subprocess.run(["explorer", str(paths["project_dir"])])
            else:  # macOS
                subprocess.run(["open", str(paths["project_dir"])])
            print("✅ Project directory opened!")
        except Exception as e:
            print(f"❌ Could not open directory: {e}")
            
        input("\nPress Enter to continue...")
    
    def clean_project_files(self):
        """Clean non-essential project files with preview and confirmation"""
        try:
            paths = self.get_paths()
            project_dir = paths['project_dir']
            
            if not project_dir.exists():
                self._show_error_dialog("Project directory not found", 
                                       f"Cannot find project directory: {project_dir}")
                return
            
            # Initialize cleaner
            cleaner = ProjectCleaner(str(project_dir))
            
            # Show scanning progress
            self._show_scanning_dialog()
            
            # Scan project
            scan_results = cleaner.scan_project()
            
            # Show scan results and get user decisions
            cleanup_options = self._show_cleanup_preview(cleaner, scan_results)
            if cleanup_options:
                # Perform cleanup with user options
                self._perform_cleanup(cleaner, scan_results, cleanup_options)
            
        except Exception as e:
            self._show_error_dialog("Cleanup Error", f"An error occurred during cleanup: {str(e)}")
    
    def _show_scanning_dialog(self):
        """Show scanning progress dialog"""
        self.clear_screen()
        self.show_banner()
        
        border = bright_orange("+" + "="*66 + "+")
        print(f"\n{border}")
        
        title = bold(bright_orange("SCANNING PROJECT"))
        print(f"|{title.center(66 + len(title) - len('SCANNING PROJECT'))}|")
        print(border)
        
        scanning_icon = bright_orange(icons.get_icon('working'))
        print(f"| {scanning_icon} Scanning project for cleanup candidates...             |")
        print(f"| {scanning_icon} Analyzing file patterns and sizes...                  |")
        print(f"| {scanning_icon} Please wait...                                        |")
        print(border)
    
    def _show_cleanup_preview(self, cleaner: ProjectCleaner, scan_results: dict) -> dict:
        """Show cleanup preview with button-style navigation"""
        # First show the scan results
        self._display_scan_results(cleaner, scan_results)
        
        # Then show options menu with button navigation
        options = [
            f"{clean_icon()} Proceed with Cleanup",
            f"{icons.get_icon('info')} Show Detailed File List",
            f"{back_icon()} Cancel Cleanup"
        ]
        
        current_selection = 0
        
        while True:
            self._display_cleanup_options_menu(cleaner, scan_results, options, current_selection)
            
            key = self.get_key_input()
            if key == 'UP' and current_selection > 0:
                current_selection -= 1
            elif key == 'DOWN' and current_selection < len(options) - 1:
                current_selection += 1
            elif key == 'LEFT':
                if current_selection > 0:
                    current_selection -= 1
            elif key == 'RIGHT':
                if current_selection < len(options) - 1:
                    current_selection += 1
            elif key == 'ENTER':
                if current_selection == 0:  # Proceed with cleanup
                    return self._get_cleanup_options(cleaner, scan_results)
                elif current_selection == 1:  # Show detailed list
                    self._show_detailed_preview(cleaner, scan_results)
                    continue
                elif current_selection == 2:  # Cancel
                    return None
            elif key == 'ESC':
                return None
    
    def _display_scan_results(self, cleaner: ProjectCleaner, scan_results: dict):
        """Display the scan results summary"""
        self.clear_screen()
        self.show_banner()
        
        border = bright_orange("+" + "="*66 + "+")
        print(f"\n{border}")
        
        title = bold(bright_orange("PROJECT CLEANUP PREVIEW"))
        print(f"|{title.center(66 + len(title) - len('PROJECT CLEANUP PREVIEW'))}|")
        print(border)
        
        total_files = 0
        total_size = 0
        
        # Show categories and totals
        for category, data in scan_results.items():
            if data['files']:
                icon = clean_icon()
                if not cleaner.is_safe_to_delete(category):
                    icon = warning_icon()
                
                desc = cleaner.get_category_description(category)
                count = data['count']
                size_str = cleaner.format_size(data['total_size'])
                
                # Color code based on safety
                if cleaner.is_safe_to_delete(category):
                    desc_colored = orange(desc[:35])
                    count_str = bright_white(f"{count} items")
                    size_colored = bright_orange(size_str)
                else:
                    desc_colored = bright_orange(f"{desc[:35]} (CAUTION)")
                    count_str = dark_orange(f"{count} items")
                    size_colored = dark_orange(size_str)
                
                print(f"| {bright_orange(icon)} {desc_colored} | {count_str} | {size_colored} |")
                total_files += count
                total_size += data['total_size']
        
        print(border)
        
        # Show totals
        total_files_colored = bold(bright_white(str(total_files)))
        total_size_colored = bold(bright_orange(cleaner.format_size(total_size)))
        print(f"| TOTAL: {total_files_colored} files/folders, {total_size_colored} to be cleaned         |")
        print(border)
    
    def _display_cleanup_options_menu(self, cleaner: ProjectCleaner, scan_results: dict, options: list, current_selection: int):
        """Display cleanup options menu with button-style navigation"""
        # Calculate totals for display
        total_files = sum(data['count'] for data in scan_results.values() if data['files'])
        total_size = sum(data['total_size'] for data in scan_results.values() if data['files'])
        
        border = bright_orange("+" + "="*66 + "+")
        print(f"\n{border}")
        
        title_text = f"CLEANUP {total_files} FILES ({cleaner.format_size(total_size)})"
        title = bold(bright_orange(title_text))
        print(f"|{title.center(66 + len(title) - len(title_text))}|")
        print(border)
        
        # Display options with selection indicator
        for i, option in enumerate(options):
            if i == current_selection:
                pointer = bright_orange(pointer_icon())
                option_colored = bold(bright_white(option))
                line = f"| {pointer} {option_colored}"
                visible_length = len(f"| {pointer_icon()} {option}")
                padding = " " * (66 - visible_length)
                print(f"{line}{padding} |")
            else:
                option_colored = orange(option)
                line = f"|   {option_colored}"
                visible_length = len(f"|   {option}")
                padding = " " * (66 - visible_length)
                print(f"{line}{padding} |")
        
        print(border)
        
        # Navigation info
        nav_info = dark_orange("↑↓WS=Move | Enter=Select | ESC=Cancel")
        nav_line = f"| {nav_info}"
        nav_padding = " " * (66 - len("| ↑↓WS=Move | Enter=Select | ESC=Cancel"))
        print(f"{nav_line}{nav_padding} |")
        print(border)
    
    def _get_cleanup_options(self, cleaner: ProjectCleaner, scan_results: dict) -> dict:
        """Get user options for backup and cleanup preferences"""
        options = [
            f"{icons.get_icon('save')} Create Backup List",
            f"{clean_icon()} Skip Backup (Save Space)",
            f"{back_icon()} Cancel Cleanup"
        ]
        
        current_selection = 0
        
        while True:
            self.clear_screen()
            self.show_banner()
            
            border = bright_orange("+" + "="*66 + "+")
            print(f"\n{border}")
            
            title = bold(bright_orange("BACKUP OPTIONS"))
            print(f"|{title.center(66 + len(title) - len('BACKUP OPTIONS'))}|")
            print(border)
            
            # Info about backup
            print(f"| {icons.get_icon('info')} Backup list records what files will be deleted        |")
            print(f"| {icons.get_icon('info')} Useful for recovery if needed later                  |")
            print(f"| {warning_icon()} Skipping backup saves disk space but no recovery        |")
            print(border)
            
            # Display options
            for i, option in enumerate(options):
                if i == current_selection:
                    pointer = bright_orange(pointer_icon())
                    option_colored = bold(bright_white(option))
                    line = f"| {pointer} {option_colored}"
                    visible_length = len(f"| {pointer_icon()} {option}")
                    padding = " " * (66 - visible_length)
                    print(f"{line}{padding} |")
                else:
                    option_colored = orange(option)
                    line = f"|   {option_colored}"
                    visible_length = len(f"|   {option}")
                    padding = " " * (66 - visible_length)
                    print(f"{line}{padding} |")
            
            print(border)
            nav_info = dark_orange("↑↓WS=Move | Enter=Select | ESC=Cancel")
            nav_line = f"| {nav_info}"
            nav_padding = " " * (66 - len("| ↑↓WS=Move | Enter=Select | ESC=Cancel"))
            print(f"{nav_line}{nav_padding} |")
            print(border)
            
            key = self.get_key_input()
            if key == 'UP' and current_selection > 0:
                current_selection -= 1
            elif key == 'DOWN' and current_selection < len(options) - 1:
                current_selection += 1
            elif key == 'LEFT':
                if current_selection > 0:
                    current_selection -= 1
            elif key == 'RIGHT':
                if current_selection < len(options) - 1:
                    current_selection += 1
            elif key == 'ENTER':
                if current_selection == 0:  # Create backup
                    return {
                        'create_backup': True,
                        'proceed': True
                    }
                elif current_selection == 1:  # Skip backup
                    return {
                        'create_backup': False,
                        'proceed': True
                    }
                elif current_selection == 2:  # Cancel
                    return None
            elif key == 'ESC':
                return None
    
    def _show_detailed_preview(self, cleaner: ProjectCleaner, scan_results: dict):
        """Show detailed file list for review"""
        self.clear_screen()
        self.show_banner()
        
        border = bright_orange("+" + "="*66 + "+")
        print(f"\n{border}")
        
        title = bold(bright_orange("DETAILED FILE LIST"))
        print(f"|{title.center(66 + len(title) - len('DETAILED FILE LIST'))}|")
        print(border)
        
        for category, data in scan_results.items():
            if data['files']:
                print(f"| {bright_orange(cleaner.get_category_description(category))}:")
                print(f"| {'-' * 62} |")
                
                # Show first 10 files as preview
                for i, file_data in enumerate(data['files'][:10]):
                    if i >= 10:
                        remaining = len(data['files']) - 10
                        print(f"|   {dark_orange(f'... and {remaining} more files')}                 |")
                        break
                    
                    file_path = str(file_data['path'].relative_to(cleaner.project_root))
                    file_size = cleaner.format_size(file_data['size'])
                    
                    # Truncate long paths
                    if len(file_path) > 45:
                        file_path = file_path[:42] + "..."
                    
                    print(f"|   {orange(file_path[:45])} ({bright_white(file_size)}) |")
                
                print(f"| {' ' * 64} |")
        
        print(border)
        input(f"{dark_orange('Press Enter to continue...')}")
    
    def _perform_cleanup(self, cleaner: ProjectCleaner, scan_results: dict, cleanup_options: dict):
        """Perform the actual cleanup with progress indication"""
        self.clear_screen()
        self.show_banner()
        
        border = bright_orange("+" + "="*66 + "+")
        print(f"\n{border}")
        
        title = bold(bright_orange("CLEANING PROJECT"))
        print(f"|{title.center(66 + len(title) - len('CLEANING PROJECT'))}|")
        print(border)
        
        total_deleted_files = 0
        total_deleted_size = 0
        backup_file = None
        
        # Create backup if requested
        if cleanup_options['create_backup']:
            backup_file = cleaner.create_backup_list(scan_results)
            print(f"| {bright_orange(icons.get_icon('save'))} Backup list created: {Path(backup_file).name[:35]}... |")
        else:
            print(f"| {bright_orange(icons.get_icon('info'))} Skipping backup creation to save space...           |")
        
        print(f"| {' ' * 64} |")
        
        # Clean categories
        for category, data in scan_results.items():
            if data['files'] and cleaner.is_safe_to_delete(category):
                desc = cleaner.get_category_description(category)
                print(f"| {bright_orange(icons.get_icon('working'))} Cleaning {orange(desc[:45])}... |")
                
                deleted_count, deleted_size = cleaner.clean_category(category, data['files'])
                total_deleted_files += deleted_count
                total_deleted_size += deleted_size
                
                if deleted_count > 0:
                    size_str = cleaner.format_size(deleted_size)
                    print(f"|   {success_icon()} Removed {bright_white(str(deleted_count))} items ({bright_orange(size_str)}) |")
                else:
                    print(f"|   {warning_icon()} No files could be removed from this category |")
        
        # Clean empty directories
        print(f"| {bright_orange(icons.get_icon('working'))} Removing empty directories...                    |")
        empty_dirs_removed = cleaner.clean_empty_directories()
        if empty_dirs_removed > 0:
            print(f"|   {success_icon()} Removed {bright_white(str(empty_dirs_removed))} empty directories              |")
        else:
            print(f"|   {icons.get_icon('info')} No empty directories found                       |")
        
        print(f"| {' ' * 64} |")
        print(border)
        
        # Show final results
        total_items = total_deleted_files + empty_dirs_removed
        if total_items > 0:
            final_count = bold(bright_white(str(total_items)))
            final_size = bold(bright_orange(cleaner.format_size(total_deleted_size)))
            print(f"| {success_icon()} CLEANUP COMPLETE!                                   |")
            print(f"| {success_icon()} Removed {final_count} files/folders/directories             |")
            print(f"| {success_icon()} Freed up {final_size} of disk space                      |")
        else:
            print(f"| {warning_icon()} No files were removed                                |")
            print(f"| {icons.get_icon('info')} This may be due to permissions or files in use      |")
        
        print(border)
        
        # Show backup info
        if cleanup_options['create_backup'] and backup_file:
            print(f"| {icons.get_icon('info')} Backup list saved to: {Path(backup_file).name[:25]}...     |")
        else:
            print(f"| {icons.get_icon('info')} No backup created - more space saved!              |")
        
        print(border)
        
        input(f"\n{dark_orange('Press Enter to continue...')}")
    
    def _show_error_dialog(self, title: str, message: str):
        """Show error dialog"""
        self.clear_screen()
        self.show_banner()
        
        border = bright_orange("+" + "="*66 + "+")
        print(f"\n{border}")
        
        title_colored = bold(bright_orange(title))
        print(f"|{title_colored.center(66 + len(title_colored) - len(title))}|")
        print(border)
        
        # Split long messages
        words = message.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= 60:
                current_line += " " + word if current_line else word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        for line in lines:
            error_text = error_icon() + " " + line
            print(f"| {error_text.ljust(64)} |")
        
        print(border)
        input(f"{dark_orange('Press Enter to continue...')}")
    
    def engine_settings(self):
        """Engine settings submenu with browser-like navigation"""
        # Add to navigation history
        self.add_to_history("engine_settings", self.current_selection)
        
        options = [
            f"{icons.get_icon('show')} Show Current Settings",
            f"{icons.get_icon('update')} Update UE Version",
            f"{icons.get_icon('change')} Change UE Directory", 
            f"{back_icon()} Back to Main Menu"
        ]
        
        while True:
            self.display_menu_with_selection("ENGINE SETTINGS", options, self.current_selection)
            
            key = self.get_key_input()
            choice = None
            
            if key == 'UP' and self.current_selection > 0:
                self.current_selection -= 1
            elif key == 'DOWN' and self.current_selection < len(options) - 1:
                self.current_selection += 1
            elif key == 'LEFT':
                # Browser-like back navigation
                history_entry = self.go_back()
                if history_entry:
                    if history_entry['menu'] == 'main_menu':
                        return  # Go back to main menu
                    elif history_entry['menu'] == 'engine_settings':
                        self.current_selection = history_entry['selection']
            elif key == 'RIGHT':
                # Browser-like forward navigation
                history_entry = self.go_forward()
                if history_entry:
                    if history_entry['menu'] == 'engine_settings':
                        self.current_selection = history_entry['selection']
            elif key == 'ENTER':
                choice = self.current_selection + 1
            elif key == 'ESC':
                break
                
            if choice == 1:
                self.show_engine_settings()
            elif choice == 2:
                self.update_ue_version()
            elif choice == 3:
                self.change_ue_directory()
            elif choice == 4:
                break
    
    def show_engine_settings(self):
        """Display current engine settings"""
        self.clear_screen()
        self.show_banner()
        paths = self.get_paths()
        print("\n📋 Current Engine Settings:")
        print("="*40)
        print(f"UE Version: {self.config['ue_version']}")
        print(f"UE Directory: {self.config['ue_dir']}")
        print(f"Editor Executable: {paths['editor_exe']}")
        print(f"Build Tool: {paths['build_tool']}")
        input("\nPress Enter to continue...")
    
    def update_ue_version(self):
        """Update Unreal Engine version"""
        self.clear_screen()
        self.show_banner()
        current = self.config["ue_version"]
        new_version = input(f"Enter new UE version [{current}]: ").strip()
        
        if new_version and new_version != current:
            self.config["ue_version"] = new_version
            if self.save_config():
                print("[✓] UE version updated successfully!")
            else:
                print("[X] Failed to save configuration.")
        else:
            print("No changes made.")
            
        input("\nPress Enter to continue...")
    
    def change_ue_directory(self):
        """Change Unreal Engine directory"""
        self.clear_screen()
        self.show_banner()
        current = self.config["ue_dir"]
        print(f"Current UE directory: {current}")
        new_dir = input("Enter new UE directory: ").strip()
        
        if new_dir:
            if Path(new_dir).exists():
                self.config["ue_dir"] = new_dir
                if self.save_config():
                    print("[✓] UE directory updated and validated!")
                else:
                    print("[X] Failed to save configuration.")
            else:
                confirm = input("[!] Directory not found. Save anyway? (y/n): ")
                if confirm.lower().startswith('y'):
                    self.config["ue_dir"] = new_dir
                    if self.save_config():
                        print("[!] UE directory updated (not validated).")
                    else:
                        print("[X] Failed to save configuration.")
        else:
            print("No changes made.")
            
        input("\nPress Enter to continue...")
    
    def path_configuration(self):
        """Path configuration submenu - same as customize_config but as menu option"""
        self.clear_screen()
        self.customize_config()
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop"""
        # Show initial setup on first run or if config is invalid
        if not self.config_file.exists() or not self.config:
            self.initial_setup()
        else:
            self.clear_screen()
            self.show_banner()
        
        # Main menu loop with navigation handling
        while True:
            result = self.show_main_menu()
            
            # Handle navigation returns
            if result == "project_management":
                self.project_management()
                continue
            elif result == "engine_settings":
                self.engine_settings() 
                continue
            
            # Handle regular menu choices
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
                # Thank you message with colors
                farewell = bold(bright_orange("Thank you for using Subreal Engine Console GUI!"))
                exit_icon_colored = bright_orange(exit_icon())
                print(f"\n{exit_icon_colored} {farewell} {exit_icon_colored}")
                sys.exit(0)

def main():
    """Entry point"""
    try:
        app = SubrealGUI()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()