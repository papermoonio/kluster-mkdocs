"""
Helper module to check for duplicate models in the documentation.
"""

import re
import os
from pathlib import Path
from typing import Dict, List, Tuple, Set

# Use absolute imports instead of relative imports
from kluster_model_update.utils.file_ops import REALTIME_MD, BATCH_MD

def find_duplicate_models(filepath: Path) -> List[Tuple[str, List[str]]]:
    """
    Find duplicate model entries in a documentation file.
    
    Args:
        filepath: Path to the markdown documentation file
        
    Returns:
        List of tuples containing (model_name, [file_paths]) for duplicates
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract all examples with their include paths
        examples = re.findall(r'\?\?\? example "([^"]+)"\s+```(?:python|bash)\s+--8<-- \'([^\']+)\'', content)
        
        # Group by model name
        model_paths: Dict[str, List[str]] = {}
        for model_name, include_path in examples:
            if model_name not in model_paths:
                model_paths[model_name] = []
            model_paths[model_name].append(include_path)
        
        # Find duplicates (models with more than one path)
        duplicates = []
        for model_name, paths in model_paths.items():
            # Check if we have multiple entries of the same model for the same type (python or bash)
            python_paths = [p for p in paths if p.endswith('.py')]
            bash_paths = [p for p in paths if p.endswith('.md') or p.endswith('.sh')]
            
            if len(python_paths) > 1:
                duplicates.append((model_name, python_paths))
            if len(bash_paths) > 1:
                duplicates.append((model_name, bash_paths))
                
        return duplicates
    except Exception as e:
        print(f"Error checking for duplicates in {filepath}: {e}")
        return []

def check_matching_filenames(python_files: List[str], bash_files: List[str]) -> List[Tuple[str, str]]:
    """
    Check if Python files have corresponding Bash files with the correct extensions.
    
    Args:
        python_files: List of Python snippet file paths
        bash_files: List of Bash snippet file paths
        
    Returns:
        List of tuples containing (python_path, bash_path) for mismatched pairs
    """
    mismatched = []
    
    # Extract baseames without extensions
    python_bases = {os.path.splitext(os.path.basename(p))[0]: p for p in python_files}
    bash_bases = {os.path.splitext(os.path.basename(b))[0]: b for b in bash_files}
    
    # Check if each Python file has a matching Bash file with .md extension
    for base, python_path in python_bases.items():
        if base in bash_bases:
            bash_path = bash_bases[base]
            # Check if the Bash file has the correct .md extension
            if not bash_path.endswith('.md'):
                mismatched.append((python_path, bash_path))
    
    return mismatched

def find_inconsistent_references(markdown_file: Path) -> List[Tuple[str, str, str]]:
    """
    Find inconsistencies between model references and file paths in documentation.
    
    Args:
        markdown_file: Path to the markdown documentation file
        
    Returns:
        List of tuples containing (model_name, file_path, issue) for inconsistencies
    """
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        inconsistencies = []
        
        # Extract all examples with their include paths
        examples = re.findall(r'\?\?\? example "([^"]+)"\s+```(?:python|bash)\s+--8<-- \'([^\']+)\'', content)
        
        for model_name, include_path in examples:
            # Get just the filename part
            filename = os.path.basename(include_path)
            
            # Check for issues:
            # 1. Python include with .md extension
            if include_path.endswith('.md') and 'python' in content[content.find(include_path)-30:content.find(include_path)]:
                inconsistencies.append((model_name, include_path, "Python code block references .md file"))
            
            # 2. Bash include with .py extension
            if include_path.endswith('.py') and 'bash' in content[content.find(include_path)-30:content.find(include_path)]:
                inconsistencies.append((model_name, include_path, "Bash code block references .py file"))
            
            # 3. Bash include with .sh extension (old format)
            if include_path.endswith('.sh'):
                inconsistencies.append((model_name, include_path, "Uses outdated .sh extension instead of .md"))
                
            # 4. Mismatch between model name and filename (heuristic check)
            # Convert to lowercase and remove special characters for comparison
            clean_model = re.sub(r'[^a-z0-9]', '', model_name.lower())
            clean_filename = re.sub(r'[^a-z0-9]', '', filename.lower())
            
            # If filename doesn't contain model name at all (simplified check)
            if len(clean_model) > 3 and clean_model not in clean_filename:
                inconsistencies.append((model_name, include_path, f"Model name '{model_name}' doesn't match filename '{filename}'"))
                
        return inconsistencies
    except Exception as e:
        print(f"Error checking for inconsistencies in {markdown_file}: {e}")
        return []

def report_documentation_issues(realtime_md: Path, batch_md: Path) -> bool:
    """
    Generate a report of documentation issues that may need manual fixing.
    
    Args:
        realtime_md: Path to the real-time.md file
        batch_md: Path to the batch.md file
        
    Returns:
        True if no issues found, False if issues were found
    """
    has_issues = False
    
    # Check for duplicate models
    rt_duplicates = find_duplicate_models(realtime_md)
    batch_duplicates = find_duplicate_models(batch_md)
    
    # Check for inconsistencies
    rt_inconsistencies = find_inconsistent_references(realtime_md)
    batch_inconsistencies = find_inconsistent_references(batch_md)
    
    # Print report
    if rt_duplicates or batch_duplicates or rt_inconsistencies or batch_inconsistencies:
        has_issues = True
        print("\n⚠️ DOCUMENTATION ISSUES FOUND ⚠️")
        
        if rt_duplicates:
            print("\nDuplicate models in real-time.md:")
            for model, paths in rt_duplicates:
                print(f"  - {model}: {', '.join(paths)}")
        
        if batch_duplicates:
            print("\nDuplicate models in batch.md:")
            for model, paths in batch_duplicates:
                print(f"  - {model}: {', '.join(paths)}")
                
        if rt_inconsistencies:
            print("\nInconsistencies in real-time.md:")
            for model, path, issue in rt_inconsistencies:
                print(f"  - {model} ({path}): {issue}")
                
        if batch_inconsistencies:
            print("\nInconsistencies in batch.md:")
            for model, path, issue in batch_inconsistencies:
                print(f"  - {model} ({path}): {issue}")
                
        print("\nConsider using --clean-force to completely reset and rebuild documentation.")
        
    return not has_issues
