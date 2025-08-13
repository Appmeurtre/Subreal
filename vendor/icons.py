#!/usr/bin/env python3
"""
Beautiful terminal icons using Unicode characters
Fallback to ASCII if Unicode is not supported
"""

import sys
import locale

class Icons:
    def __init__(self):
        self.unicode_supported = self._supports_unicode()
    
    def _supports_unicode(self):
        """Check if terminal supports Unicode"""
        try:
            # Test if we can encode Unicode characters
            test_char = "●"  # Simple Unicode bullet
            test_char.encode(sys.stdout.encoding or 'utf-8')
            # Additional check for Windows console
            if sys.platform.startswith('win'):
                return False  # Force ASCII on Windows for compatibility
            return True
        except (UnicodeEncodeError, AttributeError):
            return False
    
    def get_icon(self, name):
        """Get icon by name with Unicode/ASCII fallback"""
        icons_unicode = {
            # Main menu icons
            'build': '🔨',
            'editor': '🎮', 
            'project': '📁',
            'settings': '⚙️',
            'config': '🔧',
            'exit': '❌',
            
            # Action icons
            'info': 'ℹ️',
            'validate': '🔍',
            'directory': '📂',
            'back': '⬅️',
            'forward': '➡️',
            'up': '⬆️',
            'down': '⬇️',
            
            # Status icons
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'working': '⚡',
            
            # Navigation icons
            'arrow_right': '▶',
            'arrow_left': '◀',
            'bullet': '●',
            'pointer': '👉',
            
            # Tool icons
            'show': '📋',
            'update': '🔄',
            'change': '📝',
            'save': '💾',
            'load': '📤',
            'clean': '🧹',
            'trash': '🗑️',
        }
        
        icons_ascii = {
            # Main menu icons - Windows-safe ASCII
            'build': '[#]',    # Build/hammer
            'editor': '[>]',   # Play/editor
            'project': '[+]',  # Plus/project
            'settings': '[*]', # Asterisk/settings
            'config': '[=]',   # Equals/config
            'exit': '[X]',     # X/exit
            
            # Action icons
            'info': '(i)',     # Information
            'validate': '(?)',  # Question/validate
            'directory': '[D]', # Directory
            'back': '<--',     # Back arrow
            'forward': '-->',  # Forward arrow
            'up': ' ^ ',       # Up arrow
            'down': ' v ',     # Down arrow
            
            # Status icons
            'success': '[v]',  # Check mark
            'error': '[X]',    # X mark
            'warning': '[!]',  # Warning
            'working': '[*]',  # Working
            
            # Navigation icons
            'arrow_right': '->',
            'arrow_left': '<-',
            'bullet': '*',
            'pointer': '>>',
            
            # Tool icons
            'show': '[!]',     # Show
            'update': '[^]',   # Update
            'change': '[~]',   # Change
            'save': '[S]',     # Save
            'load': '[L]',     # Load
            'clean': '[C]',    # Clean
            'trash': '[T]',    # Trash
        }
        
        if self.unicode_supported:
            return icons_unicode.get(name, f'[{name}]')
        else:
            return icons_ascii.get(name, f'[{name}]')

# Global icons instance
icons = Icons()

# Convenience functions for common icons
def build_icon():
    return icons.get_icon('build')

def editor_icon():
    return icons.get_icon('editor')

def project_icon():
    return icons.get_icon('project')

def settings_icon():
    return icons.get_icon('settings')

def config_icon():
    return icons.get_icon('config')

def exit_icon():
    return icons.get_icon('exit')

def success_icon():
    return icons.get_icon('success')

def error_icon():
    return icons.get_icon('error')

def warning_icon():
    return icons.get_icon('warning')

def back_icon():
    return icons.get_icon('back')

def forward_icon():
    return icons.get_icon('forward')

def pointer_icon():
    return icons.get_icon('pointer')

def arrow_right_icon():
    return icons.get_icon('arrow_right')

def clean_icon():
    return icons.get_icon('clean')

def trash_icon():
    return icons.get_icon('trash')