"""
Main module loader for kluster documentation update system.
This module helps manage imports and orchestrates the various components.
"""

import importlib
import sys
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Determine the base directory for all imports
BASE_DIR = Path(__file__).parent.absolute()

def import_module(module_path: str) -> Any:
    """
    Import a module from a string path.
    
    Args:
        module_path: Dot-separated path to the module
        
    Returns:
        The imported module
    """
    try:
        return importlib.import_module(module_path)
    except ImportError as e:
        raise ImportError(f"Failed to import module {module_path}: {e}")

# Core module imports
def get_model_updater():
    """Get the model table updater module."""
    return import_module("kluster_model_update.core.update_models")

# Snippet generation imports 
def get_snippets_modules():
    """Get all modules required for snippet generation."""
    modules = {
        'cli': import_module("kluster_model_update.generate_snippets.cli"),
        'api': import_module("kluster_model_update.generate_snippets.api"),
        'models': import_module("kluster_model_update.generate_snippets.models"),
        'files': import_module("kluster_model_update.generate_snippets.files"),
        'documentation': import_module("kluster_model_update.generate_snippets.documentation"),
        'main': import_module("kluster_model_update.generate_snippets.main"),
        'templates': import_module("kluster_model_update.generate_snippets.templates"),
    }
    return modules

# Utility imports
def get_check_duplicates():
    """Get the duplicate checker module."""
    return import_module("kluster_model_update.utils.check_duplicates")

def get_file_ops():
    """Get the file operations module."""
    return import_module("kluster_model_update.utils.file_ops")
