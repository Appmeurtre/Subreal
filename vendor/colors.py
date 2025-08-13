#!/usr/bin/env python3
"""
Simple terminal color module - no external dependencies
Provides ANSI color codes for terminal styling
"""

import os
import sys

# ANSI Color Codes
class Colors:
    # Reset
    RESET = '\033[0m'
    
    # Basic Colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright Colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Orange theme (#FF9800 approximation)
    ORANGE = '\033[38;5;208m'  # Closest ANSI to #FF9800
    BRIGHT_ORANGE = '\033[38;5;214m'
    DARK_ORANGE = '\033[38;5;202m'
    
    # RGB Color support (if terminal supports it)
    ORANGE_RGB = '\033[38;2;255;152;0m'  # #FF9800
    
    # Background Colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_ORANGE = '\033[48;5;208m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    STRIKETHROUGH = '\033[9m'

class ColorManager:
    def __init__(self):
        self.colors_enabled = self._supports_color()
        
    def _supports_color(self):
        """Check if terminal supports colors"""
        # Windows Command Prompt check
        if os.name == 'nt':
            # Enable ANSI escape sequences on Windows 10+
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
                return True
            except:
                return False
        
        # Unix-like systems
        return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    
    def colorize(self, text, color_code):
        """Apply color to text if colors are supported"""
        if self.colors_enabled:
            return f"{color_code}{text}{Colors.RESET}"
        return text
    
    def orange(self, text):
        """Apply orange color to text"""
        return self.colorize(text, Colors.ORANGE_RGB)
    
    def bright_orange(self, text):
        """Apply bright orange color to text"""
        return self.colorize(text, Colors.BRIGHT_ORANGE)
    
    def dark_orange(self, text):
        """Apply dark orange color to text"""
        return self.colorize(text, Colors.DARK_ORANGE)
    
    def bold(self, text):
        """Apply bold style to text"""
        return self.colorize(text, Colors.BOLD)
    
    def underline(self, text):
        """Apply underline style to text"""
        return self.colorize(text, Colors.UNDERLINE)
    
    def bright_white(self, text):
        """Apply bright white color to text"""
        return self.colorize(text, Colors.BRIGHT_WHITE)

# Global color manager instance
color_manager = ColorManager()

# Convenience functions
def orange(text):
    return color_manager.orange(text)

def bright_orange(text):
    return color_manager.bright_orange(text)

def dark_orange(text):
    return color_manager.dark_orange(text)

def bold(text):
    return color_manager.bold(text)

def underline(text):
    return color_manager.underline(text)

def bright_white(text):
    return color_manager.bright_white(text)