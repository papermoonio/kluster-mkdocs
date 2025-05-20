"""
Main functionality for generate_snippets module.
"""

import os
from typing import Dict, List, Any, Optional, Tuple, Set

from .api import fetch_models_from_api
from .models import get_model_info
from .files import (
    get_existing_models,
    REALTIME_DIR, 
    BATCH_DIR
)
from .templates import (
    get_real_time_template,
    get_batch_template,
    get_real_time_bash_template,
    get_batch_bash_template
)
from .documentation import update_documentation_files, fix_documentation_formatting

def create_snippet_files(model: Dict[str, Any], 
                         existing_real_time: List[str], 
                         existing_batch: List[str],
                         replace_all: bool = False) -> Tuple[bool, bool]:
    """Create snippet files for a model.
    
    Args:
        model: Model information dictionary
        existing_real_time: List of existing real-time model slugs
        existing_batch: List of existing batch model slugs
        replace_all: Whether to replace all existing snippets without asking
    
    Returns:
        Tuple of (real_time_created, batch_created) booleans
    """
    file_slug = model["file_slug"]
    model_id = model["id"]
    display_name = model["display_name"]
    
    real_time_created = False
    batch_created = False
    
    # Check if real-time snippet exists
    replace_real_time = True
    if file_slug in existing_real_time:
        if replace_all:
            # Auto-replace without asking
            replace_real_time = True
        else:
            # Ask user if they want to replace existing files
            print(f"ℹ Real-time example for {display_name} already exists")
            replace_confirm = input(f"  Do you want to replace the existing real-time snippets for {display_name}? (y/N): ")
            replace_real_time = replace_confirm.lower() == 'y'
            if not replace_real_time:
                print(f"  Skipping real-time example for {display_name}")
    
    if replace_real_time:
        # Create real-time Python snippet
        real_time_py_path = os.path.join(REALTIME_DIR, f"real-time-{file_slug}.py")
        real_time_py_content = get_real_time_template(model)
        
        try:
            with open(real_time_py_path, "w", encoding="utf-8") as f:
                f.write(real_time_py_content)
            action = "Replaced" if file_slug in existing_real_time else "Created"
            print(f"✓ {action} real-time Python example for {display_name}: {real_time_py_path}")
            real_time_created = True
        except Exception as e:
            print(f"✗ Error creating real-time Python example for {display_name}: {e}")
        
        # Create real-time Bash snippet (as .md file)
        real_time_bash_path = os.path.join(REALTIME_DIR, f"real-time-{file_slug}.md")
        real_time_bash_content = get_real_time_bash_template(model)
        
        try:
            with open(real_time_bash_path, "w", encoding="utf-8") as f:
                f.write(real_time_bash_content)
            action = "Replaced" if file_slug in existing_real_time else "Created"
            print(f"✓ {action} real-time Bash example for {display_name}: {real_time_bash_path}")
        except Exception as e:
            print(f"✗ Error creating real-time Bash example for {display_name}: {e}")
    
    # Check if batch snippet exists
    replace_batch = True
    if file_slug in existing_batch:
        if replace_all:
            # Auto-replace without asking
            replace_batch = True
        else:
            # Ask user if they want to replace existing files
            print(f"ℹ Batch example for {display_name} already exists")
            replace_confirm = input(f"  Do you want to replace the existing batch snippets for {display_name}? (y/N): ")
            replace_batch = replace_confirm.lower() == 'y'
            if not replace_batch:
                print(f"  Skipping batch example for {display_name}")
    
    if replace_batch:
        # Create batch Python snippet
        batch_py_path = os.path.join(BATCH_DIR, f"batch-jsonl-{file_slug}.py")
        batch_py_content = get_batch_template(model)
        
        try:
            with open(batch_py_path, "w", encoding="utf-8") as f:
                f.write(batch_py_content)
            action = "Replaced" if file_slug in existing_batch else "Created"
            print(f"✓ {action} batch Python example for {display_name}: {batch_py_path}")
            batch_created = True
        except Exception as e:
            print(f"✗ Error creating batch Python example for {display_name}: {e}")
        
        # Create batch Bash snippet (as .md file)
        batch_bash_path = os.path.join(BATCH_DIR, f"batch-jsonl-{file_slug}.md")
        batch_bash_content = get_batch_bash_template(model)
        
        try:
            with open(batch_bash_path, "w", encoding="utf-8") as f:
                f.write(batch_bash_content)
            action = "Replaced" if file_slug in existing_batch else "Created"
            print(f"✓ {action} batch Bash example for {display_name}: {batch_bash_path}")
        except Exception as e:
            print(f"✗ Error creating batch Bash example for {display_name}: {e}")
    
    return real_time_created, batch_created
