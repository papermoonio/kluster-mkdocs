"""
This module contains the generate_snippets functionality for kluster.ai documentation.
It can be imported by other scripts like update_models.py or run standalone.
"""

# Re-export main functions for importing
from .api import fetch_models_from_api
from .models import get_model_info, convert_to_slug
from .files import get_existing_models
from .templates import (
    get_real_time_template,
    get_batch_template,
    get_real_time_bash_template,
    get_batch_bash_template
)
from .documentation import update_documentation_files, fix_documentation_formatting
from .main import create_snippet_files

__version__ = "1.0.0"
from .api import fetch_models_from_api
from .models import get_model_info, convert_to_slug
from .files import get_existing_models
from .templates import (
    get_real_time_template,
    get_batch_template,
    get_real_time_bash_template,
    get_batch_bash_template
)
from .documentation import update_documentation_files, fix_documentation_formatting
from .main import create_snippet_files
from .cli import run_cli
