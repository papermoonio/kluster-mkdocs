"""
File operations and detection for snippet files.
"""

import os
from typing import List, Tuple

# Define paths
SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.join(SCRIPTS_DIR, "..")
SNIPPETS_DIR = os.path.join(ROOT_DIR, "kluster-docs/.snippets/code/get-started/start-building")
DOCS_DIR = os.path.join(ROOT_DIR, "kluster-docs/get-started/start-building")

# Paths to snippet directories
REALTIME_DIR = os.path.join(SNIPPETS_DIR, "real-time")
BATCH_DIR = os.path.join(SNIPPETS_DIR, "batch")

# Paths to documentation files
REALTIME_MD = os.path.join(DOCS_DIR, "real-time.md")
BATCH_MD = os.path.join(DOCS_DIR, "batch.md")

def get_existing_models() -> Tuple[List[str], List[str]]:
    """Get lists of existing model files.
    
    Returns:
        A tuple containing (real_time_models, batch_models) lists of slugs.
    """
    real_time_models = []
    batch_models = []
    
    # Check real-time directory
    if os.path.exists(REALTIME_DIR):
        for file in os.listdir(REALTIME_DIR):
            if file.startswith("real-time-") and file.endswith(".py"):
                model_slug = file[len("real-time-"):-3]
                real_time_models.append(model_slug)
            # Also check alternate pattern (just in case)
            elif file.startswith("realtime-") and file.endswith(".py"):
                model_slug = file[len("realtime-"):-3]
                real_time_models.append(model_slug)
    else:
        print(f"Warning: Real-time snippets directory not found, will create: {REALTIME_DIR}")
        os.makedirs(REALTIME_DIR, exist_ok=True)
    
    # Check batch directory
    if os.path.exists(BATCH_DIR):
        for file in os.listdir(BATCH_DIR):
            if file.startswith("batch-jsonl-") and file.endswith(".py"):
                model_slug = file[len("batch-jsonl-"):-3]
                batch_models.append(model_slug)
            # Also check alternate pattern (just in case)
            elif file.startswith("batch-") and file.endswith(".py") and not file.startswith("batch-jsonl-"):
                model_slug = file[len("batch-"):-3]
                batch_models.append(model_slug)
    else:
        print(f"Warning: Batch snippets directory not found, will create: {BATCH_DIR}")
        os.makedirs(BATCH_DIR, exist_ok=True)
    
    print(f"Found {len(real_time_models)} existing real-time examples and {len(batch_models)} existing batch examples")
    return real_time_models, batch_models

def migrate_sh_to_md():
    """Migrate any existing .sh files to .md files.
    
    This is a one-time migration function to handle legacy files.
    """
    migrated_count = 0
    
    # Check real-time directory