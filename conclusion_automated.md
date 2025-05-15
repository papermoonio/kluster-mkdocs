# Model Onboarding Documentation for kluster.ai Platform

## Overview

This document details the process for onboarding new models to the kluster.ai platform documentation. We've implemented an automated solution that handles all aspects of model onboarding, while keeping the manual process documentation for reference.

## Automated Solution

We've implemented an automated solution that handles all aspects of model onboarding. The solution consists of two main scripts:

1. `update_models.py`: Updates model tables in the documentation (already existed)
2. `generate_snippets.py`: Generates code snippets for new models (newly created)

These scripts work together to ensure that when new models are added to the kluster.ai API, they're automatically added to both:
- Model tables in the documentation 
- Code examples for real-time and batch inference

### How to Use the Automated Solution

Simply run the update_models.py script, which now automatically calls generate_snippets.py:

```bash
cd /path/to/kluster-mkdocs
python scripts/update_models/update_models.py
```

This will:
1. Fetch the latest models from the kluster.ai API
2. Update the model tables in `kluster-docs/get-started/models.md`
3. Update the rate limit tables in `kluster-docs/.snippets/text/get-started/rate-limit.md`
4. Detect which models don't have code examples yet
5. Generate code examples for both real-time and batch inference for those models
6. Update the documentation files to include these new examples

### Command Line Options

The automated solution supports several command line options:

```bash
# Skip generating code snippets (only update tables)
python scripts/update_models/update_models.py --skip-snippets

# Check for new models but don't create snippets (dry run)
python scripts/update_models/update_models.py --dry-run-snippets

# Run only the snippet generation step
python scripts/update_models/generate_snippets.py

# Check what snippets would be generated without creating files
python scripts/update_models/generate_snippets.py --dry-run
```

### Technical Details

The `generate_snippets.py` script:

1. Fetches models from the kluster.ai API
2. Compares the list with existing snippet files to identify new models
3. Creates four template files for each new model:
   - Python real-time example (`real-time-{model-slug}.py`)
   - Bash real-time example (`real-time-{model-slug}.md`)
   - Python batch example (`batch-jsonl-{model-slug}.py`)
   - Bash batch example (`batch-jsonl-{model-slug}.md`)
4. Updates the documentation files to include these examples in the dropdowns

The script offers several advanced features:

- **Intelligent model ID mapping**: Converts full model IDs (like `klusterai/Meta-Llama-3.1-8B-Instruct-Turbo`) to consistent, shortened slugs (like `llama3.1-8`) matching existing naming patterns
- **Multimodal model detection**: Automatically identifies models with vision capabilities and generates appropriate examples with image inputs
- **Support for alternative naming patterns**: Handles variations in file naming to avoid duplicates
- **Dry run mode**: Tests what would be generated without creating any files
- **Comprehensive error handling**: Gracefully handles API issues, file access problems, and other potential errors

All templates are standardized while still respecting the unique capabilities of each model type.

## Manual Process (Reference)

Below is the manual process that was used before automation, kept for reference.

### File Structure

When manually onboarding a new model, you need to create or modify files in the following directories:

```
/Users/franzuzz/code/kluster-mkdocs/kluster-docs/.snippets/code/get-started/start-building/
├── batch/
│   ├── batch-jsonl-{model-name}.md      # Bash example for batch inference
│   └── batch-jsonl-{model-name}.py      # Python example for batch inference
└── real-time/
    ├── real-time-{model-name}.md        # Bash example for real-time inference
    └── real-time-{model-name}.py        # Python example for real-time inference
```

Additionally, you need to update the following Markdown files to include the new model in the documentation:

```
/Users/franzuzz/code/kluster-mkdocs/kluster-docs/get-started/start-building/
├── batch.md       # Documentation for batch inference 
└── real-time.md   # Documentation for real-time inference
```

### Step 1: Create Example Files

For each model, you need to create four example files:
1. A Python real-time inference example
2. A Bash/cURL real-time inference example
3. A Python batch inference example
4. A Bash/cURL batch inference example

### Step 2: Update Documentation Files

After creating the example files, you need to update the `real-time.md` and `batch.md` files to include the new model in the dropdown menus.

### Naming Conventions

When creating files and references for a new model, follow these conventions:

1. **File naming**: Use lowercase for all filenames, with hyphens separating words
   - For real-time: `real-time-{model-name}.py` and `real-time-{model-name}.md`
   - For batch: `batch-jsonl-{model-name}.py` and `batch-jsonl-{model-name}.md`

2. **Model ID in code**: Always use the exact, case-sensitive model ID (e.g., `mistralai/Mistral-Nemo-Instruct-2407`)

3. **Display name in documentation**: Use the human-readable name with proper capitalization (e.g., `Mistral Nemo Instruct 2407`)

## Conclusion

The automated solution we've implemented significantly reduces the time and effort required to onboard new models to the kluster.ai platform documentation. By automating both the table updates and code snippet generation, we ensure that:

1. New models are immediately available in the documentation
2. Code examples are consistent across all models
3. Resources aren't wasted by generating duplicate examples
4. The onboarding process is fast and error-free
5. Multimodal models are handled appropriately with vision examples
6. File naming conventions are consistent with existing patterns
7. Documentation remains up-to-date without manual intervention

This automation represents a significant improvement in the documentation maintenance workflow, allowing the team to focus on other valuable tasks while ensuring that users always have access to the latest models with proper examples.

The automated solution is now the recommended way to onboard new models, but the manual process is documented for reference or in case of special needs.
