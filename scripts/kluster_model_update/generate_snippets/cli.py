"""
Command-line interface for the generate_snippets module.
"""

import argparse
import sys
from typing import List, Dict, Any, Optional

from .api import fetch_models_from_api
from .models import get_model_info
from .files import get_existing_models
from .documentation import update_documentation_files, fix_documentation_formatting

def create_cli_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate code snippets for Kluster.ai documentation."
    )
    parser.add_argument(
        '--model-id', 
        type=str, 
        help='Generate snippets for a specific model ID only'
    )
    parser.add_argument(
        '--fix-formatting', 
        action='store_true',
        help='Fix formatting issues in documentation files'
    )
    parser.add_argument(
        '--api-only', 
        action='store_true',
        help='Only fetch models from API without generating snippets'
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true',
        help='Print what would be done without actually doing it'
    )
    parser.add_argument(
        '--debug', 
        action='store_true',
        help='Print additional debug information'
    )
    # parser.add_argument(
    #     '--clean-force',
    #     action='store_true',
    #     help='WARNING: Dangerous option! Deletes all existing snippets and regenerates only for current API models'
    # )
    
    return parser

def parse_cli_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = create_cli_parser()
    return parser.parse_args(args)

def run_cli(args: Optional[List[str]] = None) -> int:
    """Run the CLI with the given arguments."""
    parsed_args = parse_cli_args(args)
    
    # Set debug flag
    debug = parsed_args.debug
    
    # Fix formatting if requested
    if parsed_args.fix_formatting:
        print("Fixing documentation formatting...")
        fix_documentation_formatting()
        if parsed_args.api_only:
            return 0
    
    # Fetch models from API
    print("Fetching models from Kluster API...")
    try:
        models_data = fetch_models_from_api()
        print(f"✓ Found {len(models_data)} models in the API")
    except Exception as e:
        print(f"✗ Error fetching models: {e}")
        return 1
    
    # Process models
    print("Processing model information...")
    models_info = get_model_info(models_data)
    print(f"✓ Processed {len(models_info)} models")
    
    # Filter for specific model if requested
    if parsed_args.model_id:
        model_id = parsed_args.model_id
        models_info = [m for m in models_info if m["id"] == model_id]
        if not models_info:
            print(f"✗ Model ID '{model_id}' not found in API response")
            return 1
        print(f"✓ Filtered for model: {model_id}")
    
    # Return if API-only mode
    if parsed_args.api_only:
        print("API-only mode, exiting")
        if debug:
            for model in models_info:
                print(f"- {model['id']} ({model['display_name']})")
        return 0
    
    # Get existing models
    print("Checking for existing snippet files...")
    real_time_models, batch_models = get_existing_models()
    
    # For dry run, just print what would be done
    if parsed_args.dry_run:
        print("\nDRY RUN - No changes will be made\n")
        for model in models_info:
            model_id = model["id"]
            display_name = model["display_name"]
            file_slug = model["file_slug"]
            
            rt_exists = file_slug in real_time_models
            batch_exists = file_slug in batch_models
            
            print(f"Model: {display_name} ({model_id})")
            print(f"  - Real-time snippet: {'Already exists' if rt_exists else 'Would create'}")
            print(f"  - Batch snippet: {'Already exists' if batch_exists else 'Would create'}")
            print(f"  - Documentation: Would {'update' if not (rt_exists and batch_exists) else 'skip'}")
        
        return 0
    
    # Handle regular run in main
    print("Ready to generate snippets")
    return 0

def cli_main() -> int:
    """Entry point for the command-line tool."""
    try:
        return run_cli()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(cli_main())
