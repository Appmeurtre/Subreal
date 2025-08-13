#!/usr/bin/env python3
"""
Project Cleaner for Unreal Engine Projects
Removes non-essential files and directories based on .gitignore/.p4ignore patterns
"""

import os
import shutil
import glob
from pathlib import Path
from typing import List, Dict, Tuple
import time

class ProjectCleaner:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.patterns_to_clean = self._get_cleanup_patterns()
        self.safe_mode = True
        
    def _get_cleanup_patterns(self) -> Dict[str, List[str]]:
        """Get cleanup patterns based on UE gitignore/p4ignore standards"""
        return {
            # Temporary and cache files
            "temp_cache": [
                "**/Binaries/**",
                "**/Intermediate/**", 
                "**/DerivedDataCache/**",
                "**/.vs/**",
                "**/.vscode/**",
                "**/obj/**",
                "**/bin/**",
                "**/*.tmp",
                "**/*.temp",
                "**/Temp/**"
            ],
            
            # Build artifacts
            "build_artifacts": [
                "**/*.pdb",
                "**/*.idb",
                "**/*.ilk",
                "**/*.obj",
                "**/*.pch",
                "**/*.tlog",
                "**/*.log",
                "**/*.iobj",
                "**/*.ipdb",
                "**/BuildLogs/**"
            ],
            
            # IDE and editor files
            "ide_files": [
                "**/*.sln",
                "**/*.vcxproj",
                "**/*.vcxproj.filters",
                "**/*.vcxproj.user",
                "**/*.xcworkspace",
                "**/*.xcodeproj",
                "**/.idea/**",
                "**/cmake-build-*/**"
            ],
            
            # Unreal Engine generated files
            "ue_generated": [
                "**/Saved/Logs/**",
                "**/Saved/Crashes/**", 
                "**/Saved/Profiling/**",
                "**/Saved/Backup/**",
                "**/Saved/Config/CrashReportClient/**",
                "**/Saved/Autosaves/**",
                "**/Saved/CollectionCache/**",
                "**/Saved/MaterialStatsCache/**",
                "**/Saved/ShaderDebugInfo/**"
            ],
            
            # Large asset caches
            "asset_cache": [
                "**/Saved/Cooked/**",
                "**/Saved/StagedBuilds/**",
                "**/Saved/AssetRegistry.bin",
                "**/Saved/CachedShaderDebugFiles/**",
                "**/Saved/Shaders/**"
            ],
            
            # Version control artifacts
            "vcs_artifacts": [
                "**/.git/**",
                "**/.svn/**",
                "**/.hg/**",
                "**/.p4root/**",
                "**/*.orig",
                "**/*.rej"
            ]
        }
    
    def scan_project(self) -> Dict[str, Dict]:
        """Scan project and categorize files that can be cleaned"""
        results = {}
        
        for category, patterns in self.patterns_to_clean.items():
            category_files = []
            total_size = 0
            
            for pattern in patterns:
                full_pattern = str(self.project_root / pattern)
                matches = glob.glob(full_pattern, recursive=True)
                
                for match in matches:
                    match_path = Path(match)
                    if match_path.exists():
                        try:
                            if match_path.is_file():
                                file_size = match_path.stat().st_size
                                category_files.append({
                                    'path': match_path,
                                    'size': file_size,
                                    'type': 'file'
                                })
                                total_size += file_size
                            elif match_path.is_dir():
                                dir_size = self._get_directory_size(match_path)
                                category_files.append({
                                    'path': match_path,
                                    'size': dir_size,
                                    'type': 'directory'
                                })
                                total_size += dir_size
                        except (OSError, PermissionError):
                            # Skip files we can't access
                            continue
            
            results[category] = {
                'files': category_files,
                'total_size': total_size,
                'count': len(category_files)
            }
        
        return results
    
    def _get_directory_size(self, directory: Path) -> int:
        """Calculate total size of directory"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = Path(dirpath) / filename
                    try:
                        total_size += filepath.stat().st_size
                    except (OSError, PermissionError):
                        continue
        except (OSError, PermissionError):
            pass
        return total_size
    
    def format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    def clean_category(self, category: str, files_data: List[Dict]) -> Tuple[int, int]:
        """Clean files in a specific category"""
        deleted_count = 0
        deleted_size = 0
        
        for file_data in files_data:
            file_path = file_data['path']
            file_size = file_data['size']
            
            try:
                if file_data['type'] == 'file':
                    if file_path.exists():
                        file_path.unlink()
                        deleted_count += 1
                        deleted_size += file_size
                elif file_data['type'] == 'directory':
                    if file_path.exists():
                        shutil.rmtree(file_path)
                        deleted_count += 1
                        deleted_size += file_size
            except (OSError, PermissionError) as e:
                # Skip files we can't delete
                continue
        
        return deleted_count, deleted_size
    
    def clean_empty_directories(self) -> int:
        """Remove empty directories from the project"""
        removed_count = 0
        
        # Walk directory tree bottom-up to handle nested empty dirs
        for root, dirs, files in os.walk(self.project_root, topdown=False):
            for dirname in dirs:
                dir_path = Path(root) / dirname
                try:
                    # Only remove if directory is completely empty
                    if dir_path.exists() and not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        removed_count += 1
                except (OSError, PermissionError):
                    # Skip directories we can't access or remove
                    continue
        
        return removed_count
    
    def get_category_description(self, category: str) -> str:
        """Get human-readable description for category"""
        descriptions = {
            "temp_cache": "Temporary files and build cache",
            "build_artifacts": "Compiled binaries and build logs", 
            "ide_files": "IDE project files (can be regenerated)",
            "ue_generated": "Unreal Engine generated files",
            "asset_cache": "Cooked assets and shader cache",
            "vcs_artifacts": "Version control system files"
        }
        return descriptions.get(category, category.replace('_', ' ').title())
    
    def is_safe_to_delete(self, category: str) -> bool:
        """Check if category is safe to delete without losing work"""
        safe_categories = [
            "temp_cache", 
            "build_artifacts", 
            "ue_generated", 
            "asset_cache"
        ]
        return category in safe_categories
    
    def create_backup_list(self, scan_results: Dict) -> str:
        """Create a backup list of files that will be deleted"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_file = self.project_root / f"cleanup_backup_{timestamp}.txt"
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(f"Subreal Project Cleanup Backup List\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Project: {self.project_root}\n")
            f.write("="*60 + "\n\n")
            
            for category, data in scan_results.items():
                if data['files']:
                    f.write(f"Category: {self.get_category_description(category)}\n")
                    f.write(f"Files: {data['count']}, Size: {self.format_size(data['total_size'])}\n")
                    f.write("-" * 40 + "\n")
                    
                    for file_data in data['files']:
                        f.write(f"{file_data['type']}: {file_data['path']}\n")
                    f.write("\n")
        
        return str(backup_file)