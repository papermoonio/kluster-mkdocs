"""
kluster-docs - Documentation Update Tool

A unified command-line tool for updating all kluster.ai documentation components:
1. Model tables (models.md, rate-limits.md)
2. Code snippets (real-time and batch examples)
3. Rate limit information

This script serves as a single entry point to update any or all documentation
components after API changes, new model releases, or when fixing formatting issues.
"""

import os
import sys
import glob
import argparse
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Determine directory to find modules
parts = str(Path(__file__).resolve()).split(os.sep)
assert "kluster-mkdocs" in parts, "'kluster-mkdocs' not found in path"
BASE_DIR = Path(os.sep.join(parts[:parts.index("kluster-mkdocs")+1]))

# Add the parent directory to the path to ensure imports work
sys.path.insert(0, str(BASE_DIR.parent))

def update_model_tables(dry_run: bool = False) -> bool:
    """Update model tables using update_models.py functionality."""
    try:
        # Import the module loader
        sys.path.insert(0, str(BASE_DIR))
        from core.update_models import (
            fetch_models_from_api, 
            extract_model_info, 
            update_models_md, 
            update_rate_limit_md,
            MODELS_MD_PATH,
            RATE_LIMIT_MD_PATH
        )
        
        # Call only the part that updates tables, not the snippet generation
        print("\n" + "=" * 80)
        print("UPDATING MODEL TABLES")
        print("=" * 80)
        
        # Fetch models from API
        print("🔄 Fetching models from API...")
        models_raw = fetch_models_from_api()
        
        # Process model information
        print("🔄 Processing model information...")
        models_info = extract_model_info(models_raw)
        
        if dry_run:
            print("\nDRY RUN - Model table updates would affect these files:")
            models_path = os.path.join(BASE_DIR, MODELS_MD_PATH)
            limits_path = os.path.join(BASE_DIR, RATE_LIMIT_MD_PATH)
            print(f"  - {models_path}")
            print(f"  - {limits_path}")
            print(f"  - Would update information for {len(models_info)} models\n")
            return True
        
        # Update documentation files
        print("🔄 Updating documentation files...")
        models_path = os.path.join(BASE_DIR, MODELS_MD_PATH)
        limits_path = os.path.join(BASE_DIR, RATE_LIMIT_MD_PATH)
        
        update_models_md(models_info, models_path)
        update_rate_limit_md(models_info, limits_path)
        
        print("✅ Model tables updated successfully!")
        return True
    
    except Exception as e:
        print(f"❌ Error updating model tables: {e}")
        if '--debug' in sys.argv:
            traceback.print_exc()
        return False

def generate_code_snippets(
    model_id: Optional[str] = None, 
    dry_run: bool = False,
    fix_formatting: bool = False,
    api_only: bool = False,
    debug: bool = False,
    clean_force: bool = False,
    replace_all: bool = False
) -> bool:
    """Generate code snippets using generate_snippets functionality."""
    try:
        # Add the current directory to path to ensure imports work
        sys.path.insert(0, str(BASE_DIR))
        
        # Import directly from the generate_snippets package
        from generate_snippets.cli import parse_cli_args, run_cli
        from generate_snippets.api import fetch_models_from_api
        from generate_snippets.models import get_model_info
        from generate_snippets.files import get_existing_models, REALTIME_DIR, BATCH_DIR
        from generate_snippets.documentation import update_documentation_files, fix_documentation_formatting, clean_documentation, rebuild_documentation
        from generate_snippets.main import create_snippet_files
        
        # Import duplicate checker if needed
        if debug:
            # Use absolute import for check_duplicates
            from kluster_model_update.utils.check_duplicates import report_documentation_issues
        
        print("\n" + "=" * 80)
        print("GENERATING CODE SNIPPETS")
        print("=" * 80)
        
        # Prepare arguments
        cmd_args = []
        if model_id:
            cmd_args.extend(["--model-id", model_id])
        if dry_run:
            cmd_args.append("--dry-run")
        if fix_formatting:
            cmd_args.append("--fix-formatting")
        if api_only:
            cmd_args.append("--api-only")
        if debug:
            cmd_args.append("--debug")
        if clean_force:
            cmd_args.append("--clean-force")
        
        # Parse arguments
        args = parse_cli_args(cmd_args)
        
        # Process snippets using the same logic as run_cli but imported directly
        
        # Fix formatting if requested
        if fix_formatting:
            print("Fixing documentation formatting...")
            fix_documentation_formatting()
            if api_only:
                return True
        
        # Check for duplication issues in documentation if debug mode is on
        if debug:
            from kluster_model_update.utils.file_ops import REALTIME_MD, BATCH_MD
            print("\nChecking documentation for inconsistencies...")
            report_documentation_issues(REALTIME_MD, BATCH_MD)
        
        # Fetch models from API
        print("Fetching models from Kluster API...")
        try:
            models_data = fetch_models_from_api()
            print(f"✓ Found {len(models_data)} models in the API")
        except Exception as e:
            print(f"✗ Error fetching models: {e}")
            return False
        
        # Process models
        print("Processing model information...")
        models_info = get_model_info(models_data)
        print(f"✓ Processed {len(models_info)} models")
        
        # Filter for specific model if requested
        if model_id:
            models_info = [m for m in models_info if m["id"] == model_id]
            if not models_info:
                print(f"✗ Model ID '{model_id}' not found in API response")
                return False
            print(f"✓ Filtered for model: {model_id}")
        
        # Return if API-only mode
        if api_only:
            print("API-only mode, exiting")
            if debug:
                for model in models_info:
                    print(f"- {model['id']} ({model['display_name']})")
            return True
        
        # Get existing models
        print("Checking for existing snippet files...")
        real_time_models, batch_models = get_existing_models()
        
        # Clean-force mode: Remove all existing snippet files before regenerating
        if clean_force:
            print("\n⚠️ CLEAN-FORCE MODE ACTIVATED ⚠️")
            print("⚠️ This will delete ALL existing snippet files and regenerate ONLY current API models ⚠️")
            print("⚠️ This will also reset ALL documentation references ⚠️")
            
            if dry_run:
                print("\nDRY RUN - Would delete all files in:")
                print(f"  - {REALTIME_DIR}")
                print(f"  - {BATCH_DIR}")
                print("  - Would reset all documentation references in real-time.md and batch.md")
                print("  - Would then regenerate snippets for all current API models")
            else:
                confirmation = input("Are you sure you want to proceed? This action cannot be undone. (y/N): ")
                if confirmation.lower() != 'y':
                    print("Operation cancelled by user.")
                    return False
                
                print("Cleaning directories...")
                # Empty the directories instead of removing them to preserve folder structure
                # Real-time directory
                real_time_files = glob.glob(os.path.join(REALTIME_DIR, "*"))
                for f in real_time_files:
                    if os.path.isfile(f):
                        os.remove(f)
                        print(f"  - Removed {f}")
                        
                # Batch directory
                batch_files = glob.glob(os.path.join(BATCH_DIR, "*"))
                for f in batch_files:
                    if os.path.isfile(f):
                        os.remove(f)
                        print(f"  - Removed {f}")
                
                # Clean documentation by removing all examples and resetting the files
                print("Resetting documentation files...")
                clean_documentation()
                
                # Reset the existing models lists since we've deleted all files
                real_time_models, batch_models = [], []
                print("✅ All existing snippet files and documentation references have been removed")
                print("\nRegenerating snippets for current API models...")
        
        # For dry run, just print what would be done
        if dry_run:
            print("\nDRY RUN - No changes will be made\n")
            for model in models_info:
                model_id = model["id"]
                display_name = model["display_name"]
                file_slug = model["file_slug"]
                
                # When clean-force is enabled, we'll regenerate everything regardless of existence
                if clean_force:
                    rt_exists = False  # Force regeneration
                    batch_exists = False  # Force regeneration
                else:
                    rt_exists = file_slug in real_time_models
                    batch_exists = file_slug in batch_models
                
                print(f"Model: {display_name} ({model_id})")
                print(f"  - Real-time snippet: {'Already exists' if rt_exists else 'Would create'}")
                print(f"  - Batch snippet: {'Already exists' if batch_exists else 'Would create'}")
                print(f"  - Documentation: Would {'update' if not (rt_exists and batch_exists) else 'skip'}")
            
            return True
        
        # Create snippets for each model
        new_models = []
        for model in models_info:
            real_time, batch = create_snippet_files(
                model, real_time_models, batch_models, replace_all=replace_all
            )
            if real_time or batch:
                new_models.append(model)
        
        # Update documentation with new models
        if new_models:
            if clean_force:
                # If we used clean_force, we need to use the special rebuild function
                # which works with empty sections
                print("Rebuilding documentation with all models...")
                rebuild_documentation(models_info)
            else:
                # Otherwise just add the new models to existing docs
                update_documentation_files(new_models)
        
        print("✅ Code snippet generation completed successfully!")
        return True
    
    except Exception as e:
        print(f"❌ Error generating code snippets: {e}")
        if '--debug' in sys.argv:
            traceback.print_exc()
        return False

def main():
    """Main entry point function."""
    parser = argparse.ArgumentParser(
        description="kluster-docs - Documentation Update Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update everything (model tables and code snippets)
  python update_docs.py
  
  # Dry run to see what would be updated
  python update_docs.py --dry-run
  
  # Only update model tables
  python update_docs.py --tables
  
  # Only generate code snippets
  python update_docs.py --snippets
  
  # Generate snippets for a specific model
  python update_docs.py --snippets --model-id kluster/llama3-8b
  
  # Replace all existing snippets without confirmation
  python update_docs.py --snippets --replace-all
  
  # Fix formatting issues in documentation
  python update_docs.py --snippets --fix-formatting
"""
    )
    
    # Define command groups
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--tables', action='store_true', help="Only update model tables (models.md, rate-limit.md)")
    group.add_argument('--snippets', action='store_true', help="Only generate code snippets")
    
    # Common options
    parser.add_argument('--dry-run', action='store_true', help="Show what would be done without making changes")
    parser.add_argument('--debug', action='store_true', help="Print additional debug information")
    
    # Snippet-specific options
    snippet_group = parser.add_argument_group('Snippet options')
    snippet_group.add_argument('--model-id', type=str, help="Generate snippets for a specific model ID only")
    snippet_group.add_argument('--fix-formatting', action='store_true', help="Fix formatting issues in documentation")
    snippet_group.add_argument('--api-only', action='store_true', help="Only fetch models from API (don't generate snippets)")
    snippet_group.add_argument('--replace-all', action='store_true', 
                              help="Replace all existing snippets without asking for confirmation")
    snippet_group.add_argument('--clean-force', action='store_true', 
                              help="WARNING: Dangerous option! Deletes all existing snippets and resets documentation references. After confirmation, completely rebuilds only using current API models.")
    
    args = parser.parse_args()
    
    # If no specific component selected, update everything
    update_tables = not args.snippets  # Update tables by default unless only snippets was specified
    update_snippets = not args.tables  # Update snippets by default unless only tables was specified
    
    success = True
    
    # Update model tables if requested
    if update_tables:
        tables_success = update_model_tables(dry_run=args.dry_run)
        success = success and tables_success
    
    # Generate code snippets if requested
    if update_snippets:
        snippets_success = generate_code_snippets(
            model_id=args.model_id,
            dry_run=args.dry_run,
            fix_formatting=args.fix_formatting,
            api_only=args.api_only,
            debug=args.debug,
            clean_force=args.clean_force,
            replace_all=args.replace_all
        )
        success = success and snippets_success
    
    if success:
        print("\n✅ Documentation update completed successfully!")
        return 0
    else:
        print("\n❌ Documentation update completed with errors.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
