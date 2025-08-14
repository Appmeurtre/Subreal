#!/usr/bin/env python3
"""
Unreal Engine Project Renamer
Handles renaming of UE projects including Blueprint-only and C++ projects
"""

import os
import json
import shutil
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import time

class ProjectRenamer:
    def __init__(self, project_root: str, current_project_name: str):
        self.project_root = Path(project_root).resolve()
        self.current_name = current_project_name
        self.project_dir = self.project_root / current_project_name
        self.uproject_path = self.project_dir / f"{current_project_name}.uproject"
        self.backup_dir = None
        
    def detect_project_type(self) -> Dict[str, any]:
        """Detect if project is Blueprint-only or C++ project"""
        result = {
            'type': 'blueprint',  # Default to blueprint
            'has_source': False,
            'has_binaries': False,
            'source_files': [],
            'modules': [],
            'build_files': []
        }
        
        # Check if project directory exists
        if not self.project_dir.exists():
            result['error'] = f"Project directory not found: {self.project_dir}"
            return result
            
        # Check if .uproject file exists
        if not self.uproject_path.exists():
            result['error'] = f"Project file not found: {self.uproject_path}"
            return result
        
        # Check for Source directory (indicates C++ project)
        source_dir = self.project_dir / "Source"
        if source_dir.exists():
            result['has_source'] = True
            result['type'] = 'cpp'
            
            # Find modules and source files
            for module_dir in source_dir.iterdir():
                if module_dir.is_dir() and not module_dir.name.startswith('.'):
                    module_name = module_dir.name
                    result['modules'].append(module_name)
                    
                    # Find .h and .cpp files
                    for ext in ['.h', '.cpp']:
                        for file in module_dir.glob(f"*{ext}"):
                            result['source_files'].append(file)
                    
                    # Find build files (.cs files)
                    for build_file in module_dir.glob("*.cs"):
                        result['build_files'].append(build_file)
        
        # Check for Binaries directory
        binaries_dir = self.project_dir / "Binaries"
        result['has_binaries'] = binaries_dir.exists()
        
        # Parse .uproject file for additional info
        try:
            with open(self.uproject_path, 'r', encoding='utf-8') as f:
                uproject_data = json.load(f)
                
            # Check if modules are defined in .uproject
            if 'Modules' in uproject_data:
                result['uproject_modules'] = [mod['Name'] for mod in uproject_data['Modules']]
                if result['uproject_modules']:
                    result['type'] = 'cpp'  # Has modules = C++ project
                    
        except (json.JSONDecodeError, IOError) as e:
            result['warning'] = f"Could not parse .uproject file: {e}"
        
        return result
    
    def validate_new_name(self, new_name: str) -> Dict[str, any]:
        """Validate the new project name"""
        result = {'valid': True, 'warnings': [], 'errors': []}
        
        # Check if name is empty or whitespace
        if not new_name or not new_name.strip():
            result['valid'] = False
            result['errors'].append("Project name cannot be empty")
            return result
        
        new_name = new_name.strip()
        
        # Check for invalid characters
        invalid_chars = '<>:"/\\|?*'
        if any(char in new_name for char in invalid_chars):
            result['valid'] = False
            result['errors'].append(f"Project name contains invalid characters: {invalid_chars}")
        
        # Check for spaces (warning, not error)
        if ' ' in new_name:
            result['warnings'].append("Project name contains spaces. Consider using underscore or camelCase.")
        
        # Check length
        if len(new_name) > 100:
            result['valid'] = False
            result['errors'].append("Project name is too long (max 100 characters)")
        
        # Check if it starts with a number
        if new_name[0].isdigit():
            result['warnings'].append("Project name starts with a number. This may cause issues with C++ compilation.")
        
        # Check if target directory already exists
        target_dir = self.project_root / new_name
        if target_dir.exists():
            result['valid'] = False
            result['errors'].append(f"Directory already exists: {target_dir}")
        
        # Check if same name
        if new_name == self.current_name:
            result['valid'] = False
            result['errors'].append("New name is the same as current name")
        
        return result
    
    def create_backup(self) -> str:
        """Create backup of the project before renaming"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_name = f"{self.current_name}_backup_{timestamp}"
        self.backup_dir = self.project_root / backup_name
        
        # Copy entire project directory
        shutil.copytree(self.project_dir, self.backup_dir)
        
        return str(self.backup_dir)
    
    def rename_project_files(self, new_name: str) -> Dict[str, any]:
        """Rename project files and update content"""
        result = {'success': True, 'changes': [], 'errors': []}
        
        try:
            # 1. Rename .uproject file
            old_uproject = self.project_dir / f"{self.current_name}.uproject"
            new_uproject = self.project_dir / f"{new_name}.uproject"
            
            if old_uproject.exists():
                old_uproject.rename(new_uproject)
                result['changes'].append(f"Renamed {old_uproject.name} → {new_uproject.name}")
            
            # 2. Update .uproject content if it has modules
            self._update_uproject_content(new_uproject, new_name, result)
            
            # 3. Update Config files
            self._update_config_files(new_name, result)
            
            # 4. Handle C++ specific changes
            project_info = self.detect_project_type()
            if project_info['type'] == 'cpp':
                self._rename_cpp_files(new_name, result)
                self._update_cpp_content(new_name, result)
            
            # 5. Clean up generated directories
            self._cleanup_generated_dirs(result)
            
        except Exception as e:
            result['success'] = False
            result['errors'].append(f"Unexpected error during renaming: {str(e)}")
            
        return result
    
    def _update_uproject_content(self, uproject_path: Path, new_name: str, result: Dict):
        """Update .uproject file content"""
        try:
            with open(uproject_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update module names in .uproject
            old_pattern = f'"{self.current_name}"'
            new_pattern = f'"{new_name}"'
            
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                
                with open(uproject_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                result['changes'].append(f"Updated module references in {uproject_path.name}")
                
        except Exception as e:
            result['errors'].append(f"Failed to update .uproject content: {e}")
    
    def _update_config_files(self, new_name: str, result: Dict):
        """Update configuration files"""
        config_dir = self.project_dir / "Config"
        if not config_dir.exists():
            return
        
        config_files = [
            "DefaultEngine.ini",
            "DefaultGame.ini", 
            "DefaultInput.ini"
        ]
        
        for config_file in config_files:
            config_path = config_dir / config_file
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    modified = False
                    
                    # Add redirect for old project name
                    if config_file == "DefaultEngine.ini":
                        # Add game name redirect
                        redirect_line = f"+ActiveGameNameRedirects=(OldGameName=\"/Script/{self.current_name}\", NewGameName=\"/Script/{new_name}\")"
                        
                        if "[/Script/Engine.Engine]" in content:
                            # Insert after existing section
                            content = content.replace(
                                "[/Script/Engine.Engine]",
                                f"[/Script/Engine.Engine]\n{redirect_line}"
                            )
                        else:
                            # Add new section
                            content += f"\n\n[/Script/Engine.Engine]\n{redirect_line}\n"
                        
                        modified = True
                    
                    # Replace project name references
                    old_refs = [
                        f"GameName={self.current_name}",
                        f"ProjectName={self.current_name}",
                        f"/Script/{self.current_name}",
                    ]
                    
                    for old_ref in old_refs:
                        new_ref = old_ref.replace(self.current_name, new_name)
                        if old_ref in content:
                            content = content.replace(old_ref, new_ref)
                            modified = True
                    
                    if modified:
                        with open(config_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        result['changes'].append(f"Updated {config_file}")
                        
                except Exception as e:
                    result['errors'].append(f"Failed to update {config_file}: {e}")
    
    def _rename_cpp_files(self, new_name: str, result: Dict):
        """Rename C++ source files"""
        source_dir = self.project_dir / "Source"
        if not source_dir.exists():
            return
        
        # Rename main project module files
        for module_dir in source_dir.iterdir():
            if module_dir.is_dir() and module_dir.name == self.current_name:
                # Rename module directory
                new_module_dir = source_dir / new_name
                module_dir.rename(new_module_dir)
                result['changes'].append(f"Renamed module directory: {self.current_name} → {new_name}")
                
                # Update module_dir reference
                module_dir = new_module_dir
            
            if module_dir.is_dir():
                # Rename files with project name
                for file_path in module_dir.iterdir():
                    if file_path.is_file() and self.current_name in file_path.name:
                        new_filename = file_path.name.replace(self.current_name, new_name)
                        new_file_path = module_dir / new_filename
                        file_path.rename(new_file_path)
                        result['changes'].append(f"Renamed: {file_path.name} → {new_filename}")
    
    def _update_cpp_content(self, new_name: str, result: Dict):
        """Update C++ file contents"""
        source_dir = self.project_dir / "Source"
        if not source_dir.exists():
            return
        
        # Update all .h, .cpp, and .cs files
        for file_path in source_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in ['.h', '.cpp', '.cs']:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    modified = False
                    
                    # Replace common patterns
                    patterns = [
                        (f'#include "{self.current_name}.h"', f'#include "{new_name}.h"'),
                        (f'IMPLEMENT_PRIMARY_GAME_MODULE.*{self.current_name}', f'IMPLEMENT_PRIMARY_GAME_MODULE(FDefaultGameModuleImpl, {new_name});'),
                        (f'{self.current_name.upper()}_API', f'{new_name.upper()}_API'),
                        (f'class {self.current_name.upper()}_API', f'class {new_name.upper()}_API'),
                        (f'"{self.current_name}"', f'"{new_name}"'),
                    ]
                    
                    for old_pattern, new_pattern in patterns:
                        if old_pattern in content:
                            content = re.sub(old_pattern, new_pattern, content)
                            modified = True
                    
                    if modified:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        result['changes'].append(f"Updated content in {file_path.relative_to(self.project_dir)}")
                        
                except Exception as e:
                    result['errors'].append(f"Failed to update {file_path}: {e}")
    
    def _cleanup_generated_dirs(self, result: Dict):
        """Clean up generated directories that need regeneration"""
        dirs_to_clean = ["Binaries", "Intermediate", "Saved/.vs"]
        
        for dir_name in dirs_to_clean:
            dir_path = self.project_dir / dir_name
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    result['changes'].append(f"Cleaned up {dir_name} directory")
                except Exception as e:
                    result['errors'].append(f"Failed to clean up {dir_name}: {e}")
    
    def rename_project_directory(self, new_name: str) -> bool:
        """Rename the project directory itself"""
        try:
            new_project_dir = self.project_root / new_name
            self.project_dir.rename(new_project_dir)
            return True
        except Exception:
            return False
    
    def rollback_changes(self) -> bool:
        """Rollback changes using backup"""
        if not self.backup_dir or not self.backup_dir.exists():
            return False
        
        try:
            # Remove current project directory if it exists
            if self.project_dir.exists():
                shutil.rmtree(self.project_dir)
            
            # Restore from backup
            shutil.copytree(self.backup_dir, self.project_dir)
            
            # Remove backup
            shutil.rmtree(self.backup_dir)
            
            return True
        except Exception:
            return False