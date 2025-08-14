#!/usr/bin/env python3
"""
Simple terminal color module - no external dependencies
Provides ANSI color codes for terminal styling
"""

import os
import sys
import re

# ANSI Color Codes
class Colors:
    # Reset
    RESET = '\033[0m'
    
    # Basic Colors - limited to complement orange theme
    WHITE = '\033[37m'
    
    # Bright Colors
    BRIGHT_WHITE = '\033[97m'
    
    # Orange theme - primary color scheme
    DARK_ORANGE = '\033[38;5;166m'    # Darker orange #D2691E
    ORANGE = '\033[38;5;208m'         # Standard orange #FF8C00
    BRIGHT_ORANGE = '\033[38;5;214m'  # Bright orange #FFA500
    LIGHT_ORANGE = '\033[38;5;215m'   # Light orange #FFAD5A
    
    # RGB Color support (if terminal supports it) - consistent orange palette
    ORANGE_RGB = '\033[38;2;255;140;0m'   # #FF8C00
    DARK_ORANGE_RGB = '\033[38;2;210;105;30m'  # #D2691E
    
    # Background Colors - orange theme only
    BG_WHITE = '\033[47m'
    BG_ORANGE = '\033[48;5;208m'
    BG_DARK_ORANGE = '\033[48;5;166m'
    
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
    
    def _get_color_code(self, color_string):
        match = re.search(r';5;(\d+)m', color_string)
        if match:
            return int(match.group(1))
        return None

    def gradient(self, text, colors):
        if not self.colors_enabled:
            return text

        color_codes = [self._get_color_code(c) for c in colors]
        if any(c is None for c in color_codes):
            return text

        gradient_text = ""
        num_colors = len(color_codes)
        len_text = len(text)

        for i, char in enumerate(text):
            ratio = i / (len_text - 1) if len_text > 1 else 0
            color_index = int(ratio * (num_colors - 1))
            
            local_ratio = (ratio * (num_colors - 1)) - color_index
            
            code1 = color_codes[color_index]
            code2 = color_codes[color_index + 1] if color_index < num_colors - 1 else color_codes[color_index]
            
            color_code = int(code1 + (code2 - code1) * local_ratio)
            gradient_text += f"\033[38;5;{color_code}m{char}"

        return gradient_text + Colors.RESET

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

def gradient_orange(text):
    return color_manager.gradient(text, [Colors.DARK_ORANGE, Colors.ORANGE, Colors.BRIGHT_ORANGE])

def light_orange(text):
    return color_manager.colorize(text, Colors.LIGHT_ORANGE)