#!/usr/bin/env python3
"""
Project Cleanup Utility
Removes Python cache files, temporary files, and other build artifacts
"""

import os
import shutil
from pathlib import Path

def cleanup_project():
    """Remove all cache and temporary files from the project"""
    
    base_dir = Path(__file__).parent
    removed_items = []
    errors = []
    
    # Patterns to remove
    patterns_to_remove = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        "**/.pytest_cache",
        "**/.mypy_cache",
        "**/*.egg-info",
        "**/.DS_Store",
        "**/Thumbs.db",
        "**/desktop.ini",
        "**/*.log",
        "**/*.bak",
        "**/*.tmp",
    ]
    
    print("🧹 Starting project cleanup...")
    print(f"📂 Base directory: {base_dir}\n")
    
    # Remove directories
    for pattern in ["**/__pycache__", "**/.pytest_cache", "**/.mypy_cache", "**/*.egg-info"]:
        for path in base_dir.glob(pattern):
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                    removed_items.append(str(path.relative_to(base_dir)))
                    print(f"✓ Removed directory: {path.relative_to(base_dir)}")
            except Exception as e:
                errors.append(f"✗ Failed to remove {path}: {e}")
    
    # Remove files
    file_patterns = ["**/*.pyc", "**/*.pyo", "**/*.pyd", "**/.DS_Store", 
                     "**/Thumbs.db", "**/desktop.ini", "**/*.bak", "**/*.tmp"]
    
    for pattern in file_patterns:
        for path in base_dir.glob(pattern):
            try:
                if path.is_file():
                    path.unlink()
                    removed_items.append(str(path.relative_to(base_dir)))
                    print(f"✓ Removed file: {path.relative_to(base_dir)}")
            except Exception as e:
                errors.append(f"✗ Failed to remove {path}: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"✨ Cleanup complete!")
    print(f"📊 Removed {len(removed_items)} items")
    
    if errors:
        print(f"\n⚠️  {len(errors)} errors occurred:")
        for error in errors:
            print(f"   {error}")
    
    print(f"{'='*60}\n")

if __name__ == "__main__":
    cleanup_project()
