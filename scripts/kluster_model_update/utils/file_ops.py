"""
Common file operations and path definitions for kluster documentation.
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional

# Base paths
SCRIPT_DIR = Path(__file__).parent.parent.absolute()
ROOT_DIR = SCRIPT_DIR.parent.parent
DOCS_ROOT = ROOT_DIR / "kluster-docs"

# Paths for documentation
SNIPPETS_DIR = DOCS_ROOT / ".snippets/code/get-started/start-building"
DOCS_DIR = DOCS_ROOT / "get-started/start-building"

# Paths for snippet directories
REALTIME_DIR = SNIPPETS_DIR / "real-time"
BATCH_DIR = SNIPPETS_DIR / "batch"

# Documentation markdown files
REALTIME_MD = DOCS_DIR / "real-time.md"
BATCH_MD = DOCS_DIR / "batch.md"
MODELS_MD = DOCS_ROOT / "models.md"
RATE_LIMITS_MD = DOCS_ROOT / "rate-limits.md"

def ensure_directory(path: Path) -> None:
    """Ensure a directory exists."""
    if not path.exists():
        path.mkdir(parents=True)
        
def get_file_list(directory: Path, extension: str = None) -> List[Path]:
    """Get a list of files in a directory, optionally filtered by extension."""
    if not directory.exists():
        return []
        
    if extension:
        return list(directory.glob(f"*.{extension}"))
    else:
        return [f for f in directory.iterdir() if f.is_file()]
