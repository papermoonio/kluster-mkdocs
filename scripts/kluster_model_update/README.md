# kluster Documentation Update Tools

This directory contains the scripts for updating the kluster.ai documentation. The unified interface handles:

1. **Model tables** - Updates `models.md` and `rate-limits.md` with the latest API data
2. **Code snippets** - Generates code examples for all models in both real-time and batch modes
3. **Documentation references** - Updates documentation to reference the generated snippets

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Troubleshooting Documentation Issues](#troubleshooting-documentation-issues)
- [Generated Files](#generated-files)
- [Development](#development)
- [Output Directories](#output-directories)
- [Modifying Snippets and Templates](#modifying-snippets-and-templates)
- [Model Vision Capability Detection](#model-vision-capability-detection)
- [Troubleshooting](#troubleshooting)

## Installation

The documentation update scripts have minimal dependencies and can run on macOS, Linux, or Windows.

### General Installation

```bash
# Install required packages
pip3 install -r requirements.txt
```

## Usage

The main entry point is `update_docs.py`, which provides a unified interface for all documentation components. There's no need to run separate scripts for different components.

### Basic Examples

```bash
# Update everything (model tables and code snippets)
python3 update_docs.py

# Only update model tables
python3 update_docs.py --tables

# Only generate code snippets
python3 update_docs.py --snippets

# Generate snippets for a specific model
python3 update_docs.py --snippets --model-id kluster/llama3-8b

# Fix formatting issues in documentation
python3 update_docs.py --snippets --fix-formatting

# Debug documentation issues and detect inconsistencies
python3 update_docs.py --snippets --debug

# Replace all existing snippets without asking for confirmation
python3 update_docs.py --snippets --replace-all

# DISABLED FROM cli.py
# # DANGEROUS: Clean and regenerate all snippets from scratch
# python3 update_docs.py --snippets --clean-force
# 
# Dry run to preview changes without making them
#python3 update_docs.py --dry-run

### Command Line Options

- `--tables`: Only update model tables (models.md, rate-limit.md)
- `--snippets`: Only generate code snippets
- `--dry-run`: Show what would be done without making changes
- `--model-id MODEL_ID`: Generate snippets for a specific model only
- `--fix-formatting`: Fix formatting issues in documentation
- `--api-only`: Only fetch models from API (don't generate snippets)
- `--replace-all`: Replace all existing snippets without asking for confirmation
- `--debug`: Print additional debug information and run documentation consistency checks
- `--clean-force`: DANGEROUS! Deletes all existing snippets and resets documentation references. After confirmation, completely rebuilds only using current API models

**Note**: By default, running `update_docs.py` without options will update both model tables and code snippets. You can use the `--tables` or `--snippets` options to update only specific components if needed.

## Directory Structure

- `update_docs.py`: Main entry point script for all documentation updates
- `README.md`: This documentation file
- `core/`: Core functionalities
  - `__init__.py`: Package initialization
  - `update_models.py`: Script for updating model tables
  - `module_loader.py`: Module loading and organization utilities
- `generate_snippets/`: Package for code snippet generation
  - `__init__.py`: Package initialization 
  - `api.py`: API interaction functions
  - `models.py`: Model data structures
  - `files.py`: File operations
  - `templates.py`: Code templates
  - `documentation.py`: Documentation updates
  - `cli.py`: Command interface
  - `main.py`: Core snippet generation logic
- `utils/`: Utility modules
  - `__init__.py`: Package initialization
  - `file_ops.py`: Common file operations
  - `check_duplicates.py`: Utilities for finding and fixing documentation inconsistencies

## Troubleshooting Documentation Issues

### Identifying Problems

The script includes comprehensive diagnostics to identify common documentation issues:

```bash
# Run with debug mode to check for inconsistencies
python3 update_docs.py --snippets --debug
```

Debug mode will detect and report:
1. **Duplicate model references** - The same model appearing multiple times
2. **File extension issues** - Bash examples using `.sh` instead of `.md` extensions
3. **Inconsistent model naming** - Model names that don't match their filenames
4. **Cross-reference errors** - Python/bash language tags referencing the wrong file types

### Fixing Issues

For minor issues, use the fix-formatting option:
```bash
python3 update_docs.py --snippets --fix-formatting
```

For more serious issues or to completely reset the documentation:
```bash
# First run a dry-run to see what would change
python3 update_docs.py --snippets --clean-force --dry-run

# Then run the actual reset (requires confirmation)
python3 update_docs.py --snippets --clean-force
```

The `--clean-force` option will:
1. Delete all existing snippet files
2. Remove all example sections from the documentation 
3. Regenerate snippets for all current API models
4. Rebuild the documentation with correct references

## Generated Files

The scripts generate several types of files:

1. **Real-time API examples:**
   - Python: `real-time-{model_slug}.py`
   - Bash: `real-time-{model_slug}.md` (Bash examples as markdown files)

2. **Batch API examples:**
   - Python: `batch-jsonl-{model_slug}.py`
   - Bash: `batch-jsonl-{model_slug}.md` (Bash examples as markdown files)

## Development

### Dependencies

The documentation update scripts maintain their own minimal set of dependencies separate from the main MkDocs project requirements. This ensures the scripts can run independently.

- **Main requirements**: `/Users/franzuzz/code/kluster-mkdocs/requirements.txt` (for the entire MkDocs project)
- **Script requirements**: `/Users/franzuzz/code/kluster-mkdocs/scripts/kluster_model_update/requirements.txt` (only for these scripts)

To update dependencies:

```bash
# Install dependencies for just the documentation update scripts
cd /Users/franzuzz/code/kluster-mkdocs/scripts/kluster_model_update
pip install -r requirements.txt

# If working with the full MkDocs site, also install main requirements
cd /Users/franzuzz/code/kluster-mkdocs
pip install -r requirements.txt
```

## Output Directories

- `kluster-docs/get-started/models.md`: The model tables markdown file
- `kluster-docs/.snippets/text/get-started/rate-limit.md`: Rate limit information file
- `kluster-docs/.snippets/code/get-started/start-building/real-time/`: Real-time code snippets directory
- `kluster-docs/.snippets/code/get-started/start-building/batch/`: Batch code snippets directory

## Modifying Snippets and Templates

### Updating Snippet Templates

Snippet templates define the structure of code examples for all models. To update these templates:

1. Edit the template functions in `generate_snippets/templates.py`:
   - `get_real_time_template()` - For Python real-time API examples
   - `get_batch_template()` - For Python batch API examples
   - `get_real_time_bash_template()` - For Bash real-time API examples
   - `get_batch_bash_template()` - For Bash batch API examples

2. After updating templates, regenerate snippets for all models:
   ```bash
   python3 update_docs.py --snippets
   ```

3. To test changes before committing, use the dry-run flag:
   ```bash
   python3 update_docs.py --snippets --dry-run
   ```

### Modifying Individual Snippets

To modify a specific model's snippet:

1. **Option 1: Direct Edit**
   - Locate the file in the appropriate directory:
     - `kluster-docs/.snippets/code/get-started/start-building/real-time/` (for real-time examples)
     - `kluster-docs/.snippets/code/get-started/start-building/batch/` (for batch examples)
   - Edit the file directly
   - This approach is suitable for model-specific customizations

2. **Option 2: Regenerate**
   - Delete the existing snippet file
   - Run the script with the specific model ID:
     ```bash
     python3 update_docs.py --snippets --model-id MODEL_ID
     ```
   - This will create a fresh snippet from the template

### Adding New Snippet Types

To add a new type of snippet (e.g., for a new API endpoint):

1. Add new template functions in `generate_snippets/templates.py`
2. Update the `create_snippet_files()` function in `generate_snippets/main.py` to generate the new snippet type
3. Update `documentation.py` to reference the new snippets in documentation files

### Tips for Maintaining Snippets

- Always use the `.py` extension for Python examples
- Always use the `.md` extension for Bash/shell examples (for MkDocs compatibility)
- Keep file naming consistent with established patterns:
  - `real-time-{model_slug}.py`
  - `real-time-{model_slug}.md`
  - `batch-jsonl-{model_slug}.py`
  - `batch-jsonl-{model_slug}.md`
- The script automatically updates documentation references, but check for proper inclusion in documentation files
- For vision-capable models, special templates are used - see the [Model Vision Capability Detection](#model-vision-capability-detection) section for details

## Troubleshooting

### Common Issues

1. **Model Not Found in API**
   - Ensure the model ID is correct
   - Check if the model is available in the API by running: `python3 update_docs.py --snippets --api-only --debug`

2. **Documentation Formatting Issues**
   - Run with the fix-formatting flag: `python3 update_docs.py --snippets --fix-formatting`
   - This resolves common issues with missing closing backticks or inconsistent formatting

3. **File Extension Problems**
   - If you find `.sh` files instead of `.md` files, this is a legacy issue
   - Delete the `.sh` files and regenerate with the current version of the script

4. **Missing References in Documentation**
   - Check that filenames match the expected patterns
   - Ensure the references in `batch.md` and `real-time.md` follow the correct format:
     ```markdown
     ??? example "Model Name"
         ```python
         --8<-- 'code/get-started/start-building/real-time/real-time-model-slug.py'
         ```
     ```

5. **Outdated or Duplicate Snippets**
   - Use the `--clean-force` option to completely regenerate all snippets: `python3 update_docs.py --snippets --clean-force`
   - WARNING: This will delete ALL existing snippets and only regenerate those for models currently in the API
   - Always run with `--dry-run` first to see what would be affected: `python3 update_docs.py --snippets --clean-force --dry-run`

### API Authentication Issues

If you encounter authentication issues when fetching from the API:
1. Check that your API key is set correctly in the environment
2. Ensure you have the necessary permissions for the API endpoints
3. Try setting the API key explicitly: `export API_KEY="your-api-key"`

### macOS Specific Issues

1. **Python Version Conflicts**
   - macOS comes with a system Python (2.7) that should not be used for development
   - Use Python from Homebrew or another package manager: `brew install python`
   - Alternatively, use pyenv to manage multiple Python versions: `brew install pyenv`

2. **Environment Variable Persistence**
   - To set API keys permanently on macOS, add to your shell profile:
     ```zsh
     # Add to ~/.zshrc (for zsh) or ~/.bash_profile (for bash)
     export API_KEY="your-api-key"
     ```
   - Then reload your shell settings: `source ~/.zshrc` or `source ~/.bash_profile`

3. **Permission Issues**
   - If you encounter permission errors when installing packages on macOS:
     ```zsh
     # Option 1: Use a virtual environment (recommended)
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     
     # Option 2: Install with user flag
     pip install --user -r requirements.txt
     ```

4. **SSL Certificate Issues**
   - If you encounter SSL errors when calling the API on macOS:
     ```zsh
     # Install certificates for Python
     pip install certifi
     # Or update your certificates
     /Applications/Python\ 3.x/Install\ Certificates.command
     ```

## Model Vision Capability Detection

The script automatically detects and generates specialized code examples for models with vision capabilities. This ensures that all generated documentation reflects each model's actual capabilities.

### How Vision Models are Detected

Vision-capable models are identified in the `models.py` file through API metadata:

```python
# Check for vision capabilities
supports_vision = (model.get("model_purpose") == "multimodal" or 
                  "vision" in model.get("tags", []))
```

A model is considered vision-capable if either:
- Its `model_purpose` is set to "multimodal", OR
- It has "vision" in its tags list

This information is stored in each model's data object and passed to the template generation functions.

### Different Templates for Vision Models

When a model supports vision capabilities, different code templates are generated:

#### Real-time Vision Templates

For vision-capable models, additional examples are included to demonstrate image input:

```python
# Example with image input
image_url = "https://github.com/kluster-ai/klusterai-cookbook/blob/main/images/parking-image.jpeg?raw=true"

vision_messages = [
    {
        "role": "user", 
        "content": [
            {"type": "text", "text": "Describe what you see in this image."},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
    }
]

vision_response = client.real_time.completions.create(
    model="model_id_here",
    messages=vision_messages,
    max_tokens=300,
)
```

#### Batch Vision Templates

For batch processing with vision models, specialized JSONL input formats are demonstrated:

```python
# Create input file with multiple image requests (JSONL format)
input_jsonl_path = "batch_input.jsonl"
with open(input_jsonl_path, "w") as f:
    # Example 1
    f.write(json.dumps({
        "messages": [
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": "Who can park in the area?"},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        "max_tokens": 300
    }) + "\n")
```

This automated differentiation ensures that users have appropriate working examples for each model type without requiring manual customization.
