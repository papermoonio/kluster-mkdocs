"""
Documentation updating functions.
"""

import re
import os
from typing import Dict, Any, List, Union

from .files import REALTIME_MD, BATCH_MD

def update_documentation_files(model: Union[Dict[str, Any], List[Dict[str, Any]]]) -> bool:
    """Update documentation files to include the new model(s) alphabetically.
    
    Args:
        model: A single model dictionary or a list of model dictionaries
    """
    # Handle both single model and list of models
    if isinstance(model, list):
        # Process each model one by one
        success = True
        for m in model:
            success = success and update_documentation_files(m)
        return success
    
    # Process a single model
    display_name = model["display_name"]
    file_slug = model["file_slug"]
    
    try:
        # Read the documentation files
        with open(REALTIME_MD, 'r', encoding='utf-8') as f:
            real_time_content = f.read()
        
        with open(BATCH_MD, 'r', encoding='utf-8') as f:
            batch_content = f.read()
        
        # Update real-time.md file
        if f'??? example "{display_name}"' in real_time_content:
            print(f"ℹ Model {display_name} already in real-time.md, skipping update")
            realtime_updated = True
        else:
            # Find all Python examples in the real-time.md file
            python_examples = re.findall(r'(\?\?\? example "([^"]+)"\s+```python\s+--8<-- \'code/get-started/start-building/real-time/[^\']+\'(?:\s+```)?)', real_time_content)
            bash_examples = re.findall(r'(\?\?\? example "([^"]+)"\s+```bash\s+--8<-- \'code/get-started/start-building/real-time/[^\']+\'(?:\s+```)?)', real_time_content)
            
            # Extract Python section (works even if there are no examples yet)
            python_section_match = re.search(r'### Python\s+\n+To use these snippets[^\n]+\n+(.+?)### CLI', real_time_content, re.DOTALL)
            if python_section_match:
                    python_section = python_section_match.group(1)
                    
                    # Create new example text with proper formatting
                    new_example = (
                        f'??? example "{display_name}"\n\n'
                        f'    ```python\n'
                        f'    --8<-- \'code/get-started/start-building/real-time/real-time-{file_slug}.py\'\n'
                        f'    ```\n'
                    )
                    
                    # Fix any existing examples with missing closing backticks
                    fixed_examples = []
                    for ex_text, name in python_examples:
                        if not ex_text.strip().endswith("```"):
                            # Add missing closing backticks
                            ex_text = ex_text.strip() + "\n    ```"
                        fixed_examples.append((name, ex_text))
                    
                    # Add new example to list and sort alphabetically
                    all_examples = fixed_examples + [(display_name, new_example)]
                    sorted_examples = sorted(all_examples, key=lambda x: x[0].lower())
                    
                    # Recreate Python section with sorted examples
                    new_python_section = "\n\n".join([ex_text for _, ex_text in sorted_examples])
                    real_time_content = real_time_content.replace(python_section.strip(), new_python_section)
                    
                    # Now handle Bash/CLI examples
                    if bash_examples:
                        cli_section_match = re.search(r'### CLI\s+\n+Similarly[^\n]+\n+(.+?)\n\n## Real-time', real_time_content, re.DOTALL)
                        if cli_section_match:
                            cli_section = cli_section_match.group(1)
                            
                            # Create new bash example with proper formatting
                            new_bash_example = (
                                f'??? example "{display_name}"\n\n'
                                f'    ```bash\n'
                                f'    --8<-- \'code/get-started/start-building/real-time/real-time-{file_slug}.md\'\n'
                                f'    ```\n'
                            )
                            
                            # Fix any existing examples with missing closing backticks
                            fixed_bash_examples = []
                            for ex_text, name in bash_examples:
                                if not ex_text.strip().endswith("```"):
                                    # Add missing closing backticks
                                    ex_text = ex_text.strip() + "\n    ```"
                                fixed_bash_examples.append((name, ex_text))
                            
                            # Add new example to list and sort alphabetically
                            all_bash_examples = fixed_bash_examples + [(display_name, new_bash_example)]
                            sorted_bash_examples = sorted(all_bash_examples, key=lambda x: x[0].lower())
                            
                            # Recreate CLI section with sorted examples
                            new_cli_section = "\n\n".join([ex_text for _, ex_text in sorted_bash_examples])
                            real_time_content = real_time_content.replace(cli_section.strip(), new_cli_section)
                    
                    # Write updated content
                    with open(REALTIME_MD, 'w', encoding='utf-8') as f:
                        f.write(real_time_content)
                    
                    print(f"✓ Updated real-time.md with {display_name} (alphabetically sorted)")
                    realtime_updated = True
            else:
                print(f"✗ Could not find Python section in real-time.md")
                realtime_updated = False
        
        # Update batch.md file
        if f'??? example "{display_name}"' in batch_content:
            print(f"ℹ Model {display_name} already in batch.md, skipping update")
            batch_updated = True
        else:
            # Find all Python examples in the batch.md file
            python_examples = re.findall(r'(\?\?\? example "([^"]+)"\s+```python\s+--8<-- \'code/get-started/start-building/batch/[^\']+\'(?:\s+```)?)', batch_content)
            bash_examples = re.findall(r'(\?\?\? example "([^"]+)"\s+```bash\s+--8<-- \'code/get-started/start-building/batch/[^\']+\'(?:\s+```)?)', batch_content)
            
            if python_examples:
                # Extract Python section
                python_section_match = re.search(r'### Python\s+\n+To use these snippets[^\n]+\n+(.+?)### CLI', batch_content, re.DOTALL)
                if python_section_match:
                    python_section = python_section_match.group(1)
                    
                    # Create new example text with proper formatting
                    new_example = (
                        f'??? example "{display_name}"\n\n'
                        f'    ```python\n'
                        f'    --8<-- \'code/get-started/start-building/batch/batch-jsonl-{file_slug}.py\'\n'
                        f'    ```\n'
                    )
                    
                    # Fix any existing examples with missing closing backticks
                    fixed_examples = []
                    for ex_text, name in python_examples:
                        if not ex_text.strip().endswith("```"):
                            # Add missing closing backticks
                            ex_text = ex_text.strip() + "\n    ```"
                        fixed_examples.append((name, ex_text))
                    
                    # Add new example to list and sort alphabetically
                    all_examples = fixed_examples + [(display_name, new_example)]
                    sorted_examples = sorted(all_examples, key=lambda x: x[0].lower())
                    
                    # Recreate Python section with sorted examples
                    new_python_section = "\n\n".join([ex_text for _, ex_text in sorted_examples])
                    batch_content = batch_content.replace(python_section.strip(), new_python_section)
                    
                    # Now handle Bash/CLI examples
                    if bash_examples:
                        cli_section_match = re.search(r'### CLI\s+\n+Similarly[^\n]+\n+(.+?)\n\n## Batch', batch_content, re.DOTALL)
                        if cli_section_match:
                            cli_section = cli_section_match.group(1)
                            
                            # Create new bash example with proper formatting
                            new_bash_example = (
                                f'??? example "{display_name}"\n\n'
                                f'    ```bash\n'
                                f'    --8<-- \'code/get-started/start-building/batch/batch-jsonl-{file_slug}.md\'\n'
                                f'    ```\n'
                            )
                            
                            # Fix any existing examples with missing closing backticks
                            fixed_bash_examples = []
                            for ex_text, name in bash_examples:
                                if not ex_text.strip().endswith("```"):
                                    # Add missing closing backticks
                                    ex_text = ex_text.strip() + "\n    ```"
                                fixed_bash_examples.append((name, ex_text))
                            
                            # Add new example to list and sort alphabetically
                            all_bash_examples = fixed_bash_examples + [(display_name, new_bash_example)]
                            sorted_bash_examples = sorted(all_bash_examples, key=lambda x: x[0].lower())
                            
                            # Recreate CLI section with sorted examples
                            new_cli_section = "\n\n".join([ex_text for _, ex_text in sorted_bash_examples])
                            batch_content = batch_content.replace(cli_section.strip(), new_cli_section)
                    
                    # Write updated content
                    with open(BATCH_MD, 'w', encoding='utf-8') as f:
                        f.write(batch_content)
                    
                    print(f"✓ Updated batch.md with {display_name} (alphabetically sorted)")
                    batch_updated = True
                else:
                    print(f"✗ Could not find Python section in batch.md")
                    batch_updated = False
            else:
                print(f"✗ Could not find examples in batch.md")
                batch_updated = False
                
        return realtime_updated and batch_updated
    except Exception as e:
        print(f"✗ Error updating documentation for {display_name}: {e}")
        return False

def fix_documentation_formatting():
    """Fix inconsistent formatting in documentation files."""
    try:
        # Read the documentation files
        with open(REALTIME_MD, 'r', encoding='utf-8') as f:
            real_time_content = f.read()
        
        with open(BATCH_MD, 'r', encoding='utf-8') as f:
            batch_content = f.read()
        
        # Fix Python examples in real-time.md
        python_examples = re.findall(r'(\?\?\? example "([^"]+)"\s+```python\s+--8<-- \'code/get-started/start-building/real-time/[^\']+\'(?:\s+```)?)', real_time_content)
        fixed_real_time = real_time_content
        
        for ex_text, name in python_examples:
            if not ex_text.strip().endswith("```"):
                # Fix the example
                fixed_ex = ex_text.strip() + "\n    ```"
                fixed_real_time = fixed_real_time.replace(ex_text, fixed_ex)
        
        # Fix bash examples in real-time.md
        bash_examples = re.findall(r'(\?\?\? example "([^"]+)"\s+```bash\s+--8<-- \'code/get-started/start-building/real-time/[^\']+\'(?:\s+```)?)', fixed_real_time)
        
        for ex_text, name in bash_examples:
            if not ex_text.strip().endswith("```"):
                # Fix the example
                fixed_ex = ex_text.strip() + "\n    ```"
                fixed_real_time = fixed_real_time.replace(ex_text, fixed_ex)
        
        # Fix Python examples in batch.md
        python_examples = re.findall(r'(\?\?\? example "([^"]+)"\s+```python\s+--8<-- \'code/get-started/start-building/batch/[^\']+\'(?:\s+```)?)', batch_content)
        fixed_batch = batch_content
        
        for ex_text, name in python_examples:
            if not ex_text.strip().endswith("```"):
                # Fix the example
                fixed_ex = ex_text.strip() + "\n    ```"
                fixed_batch = fixed_batch.replace(ex_text, fixed_ex)
        
        # Fix bash examples in batch.md
        bash_examples = re.findall(r'(\?\?\? example "([^"]+)"\s+```bash\s+--8<-- \'code/get-started/start-building/batch/[^\']+\'(?:\s+```)?)', fixed_batch)
        
        for ex_text, name in bash_examples:
            if not ex_text.strip().endswith("```"):
                # Fix the example
                fixed_ex = ex_text.strip() + "\n    ```"
                fixed_batch = fixed_batch.replace(ex_text, fixed_ex)
        
        # Ensure correct syntax highlighting for Python and bash examples
        fixed_real_time = fixed_real_time.replace("```python\n    --8<--", "```python\n    --8<--")
        fixed_real_time = fixed_real_time.replace("```bash\n    --8<--", "```bash\n    --8<--")
        fixed_batch = fixed_batch.replace("```python\n    --8<--", "```python\n    --8<--")
        fixed_batch = fixed_batch.replace("```bash\n    --8<--", "```bash\n    --8<--")
        
        # Remove any Bash formatting for Python files
        fixed_real_time = re.sub(r'```bash\s+--8<-- \'code/get-started/start-building/real-time/.*?\.py\'', 
                                lambda m: m.group(0).replace('```bash', '```python'), 
                                fixed_real_time)
        fixed_batch = re.sub(r'```bash\s+--8<-- \'code/get-started/start-building/batch/.*?\.py\'', 
                          lambda m: m.group(0).replace('```bash', '```python'), 
                          fixed_batch)
        
        # Write the fixed content back to the files
        with open(REALTIME_MD, 'w', encoding='utf-8') as f:
            f.write(fixed_real_time)
        
        with open(BATCH_MD, 'w', encoding='utf-8') as f:
            f.write(fixed_batch)
        
        print("✓ Fixed formatting in documentation files")
        return True
    except Exception as e:
        print(f"✗ Error fixing documentation formatting: {e}")
        return False

def clean_documentation(models_info=None):
    """Remove all example snippets from documentation and optionally rebuild with current models.
    
    Args:
        models_info: Optional list of model dictionaries to rebuild documentation with
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Read the documentation files
        with open(REALTIME_MD, 'r', encoding='utf-8') as f:
            real_time_content = f.read()
        
        with open(BATCH_MD, 'r', encoding='utf-8') as f:
            batch_content = f.read()
        
        # Extract the sections before and after the examples in real-time.md
        realtime_python_section_regex = re.compile(r'(### Python\s+\n+To use these snippets[^\n]+\n+)(.+?)(### CLI)', re.DOTALL)
        realtime_python_match = realtime_python_section_regex.search(real_time_content)
        
        # Extract the sections before and after the bash examples in real-time.md
        realtime_cli_section_regex = re.compile(r'(### CLI\s+\n+Similarly[^\n]+\n+)(.+?)(\n\n## Real-time)', re.DOTALL)
        realtime_cli_match = realtime_cli_section_regex.search(real_time_content)
        
        # Extract the sections before and after the examples in batch.md
        batch_python_section_regex = re.compile(r'(### Python\s+\n+To use these snippets[^\n]+\n+)(.+?)(### CLI)', re.DOTALL)
        batch_python_match = batch_python_section_regex.search(batch_content)
        
        # Extract the sections before and after the bash examples in batch.md
        batch_cli_section_regex = re.compile(r'(### CLI\s+\n+Similarly[^\n]+\n+)(.+?)(\n\n## Batch)', re.DOTALL)
        batch_cli_match = batch_cli_section_regex.search(batch_content)
        
        if not all([realtime_python_match, realtime_cli_match, batch_python_match, batch_cli_match]):
            print("✗ Could not find all required sections in documentation files")
            failed_sections = []
            if not realtime_python_match: failed_sections.append("realtime Python section")
            if not realtime_cli_match: failed_sections.append("realtime CLI section")
            if not batch_python_match: failed_sections.append("batch Python section")
            if not batch_cli_match: failed_sections.append("batch CLI section")
            print(f"  Missing sections: {', '.join(failed_sections)}")
            return False
        
        # Create empty examples sections (just a newline to maintain spacing)
        empty_examples = "\n"
        
        # Clean real-time.md
        real_time_cleaned = (
            real_time_content[:realtime_python_match.start(2)] + 
            empty_examples + 
            real_time_content[realtime_python_match.end(2):realtime_cli_match.start(2)] + 
            empty_examples + 
            real_time_content[realtime_cli_match.end(2):]
        )
        
        # Clean batch.md
        batch_cleaned = (
            batch_content[:batch_python_match.start(2)] + 
            empty_examples + 
            batch_content[batch_python_match.end(2):batch_cli_match.start(2)] + 
            empty_examples + 
            batch_content[batch_cli_match.end(2):]
        )
        
        # Write cleaned content back to files
        with open(REALTIME_MD, 'w', encoding='utf-8') as f:
            f.write(real_time_cleaned)
        
        with open(BATCH_MD, 'w', encoding='utf-8') as f:
            f.write(batch_cleaned)
        
        print("✓ Cleaned all examples from documentation files")
        
        # If models_info is provided, rebuild the documentation with these models
        if models_info:
            success = True
            if isinstance(models_info, list) and len(models_info) > 0:
                # Use the optimized rebuild function for empty sections
                model_success = rebuild_documentation(models_info)
                success = success and model_success
                
                if success:
                    print("✓ Rebuilt documentation with current models")
                else:
                    print("⚠️ Some models could not be added to documentation")
            else:
                print("ℹ No models provided for rebuilding documentation")
        
        return True
    except Exception as e:
        print(f"✗ Error cleaning documentation: {e}")
        import traceback
        traceback.print_exc()
        return False

def rebuild_documentation(models_info: List[Dict[str, Any]]) -> bool:
    """Add model examples to cleaned documentation files with empty sections.
    
    This function is an optimized version specifically designed to work with documentation 
    files that have been cleaned by the clean_documentation function.
    
    Args:
        models_info: List of model dictionaries to add to documentation
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Read the documentation files
        with open(REALTIME_MD, 'r', encoding='utf-8') as f:
            real_time_content = f.read()
        
        with open(BATCH_MD, 'r', encoding='utf-8') as f:
            batch_content = f.read()
        
        # Create examples for all models
        realtime_python_examples = []
        realtime_bash_examples = []
        batch_python_examples = []
        batch_bash_examples = []
        
        # Sort models alphabetically by display name
        sorted_models = sorted(models_info, key=lambda x: x["display_name"].lower())
        
        for model in sorted_models:
            display_name = model["display_name"]
            file_slug = model["file_slug"]
            
            # Create real-time Python example
            realtime_python_example = (
                f'??? example "{display_name}"\n\n'
                f'    ```python\n'
                f'    --8<-- \'code/get-started/start-building/real-time/real-time-{file_slug}.py\'\n'
                f'    ```\n'
            )
            realtime_python_examples.append(realtime_python_example)
            
            # Create real-time Bash example
            realtime_bash_example = (
                f'??? example "{display_name}"\n\n'
                f'    ```bash\n'
                f'    --8<-- \'code/get-started/start-building/real-time/real-time-{file_slug}.md\'\n'
                f'    ```\n'
            )
            realtime_bash_examples.append(realtime_bash_example)
            
            # Create batch Python example
            batch_python_example = (
                f'??? example "{display_name}"\n\n'
                f'    ```python\n'
                f'    --8<-- \'code/get-started/start-building/batch/batch-jsonl-{file_slug}.py\'\n'
                f'    ```\n'
            )
            batch_python_examples.append(batch_python_example)
            
            # Create batch Bash example
            batch_bash_example = (
                f'??? example "{display_name}"\n\n'
                f'    ```bash\n'
                f'    --8<-- \'code/get-started/start-building/batch/batch-jsonl-{file_slug}.md\'\n'
                f'    ```\n'
            )
            batch_bash_examples.append(batch_bash_example)
        
        # Join all examples with newlines
        realtime_python_section = "\n\n".join(realtime_python_examples)
        realtime_bash_section = "\n\n".join(realtime_bash_examples)
        batch_python_section = "\n\n".join(batch_python_examples)
        batch_bash_section = "\n\n".join(batch_bash_examples)
        
        # Find and replace the empty sections using the same regex patterns from clean_documentation
        realtime_python_section_regex = re.compile(r'(### Python\s+\n+To use these snippets[^\n]+\n+)(.+?)(### CLI)', re.DOTALL)
        realtime_cli_section_regex = re.compile(r'(### CLI\s+\n+Similarly[^\n]+\n+)(.+?)(\n\n## Real-time)', re.DOTALL)
        batch_python_section_regex = re.compile(r'(### Python\s+\n+To use these snippets[^\n]+\n+)(.+?)(### CLI)', re.DOTALL)
        batch_cli_section_regex = re.compile(r'(### CLI\s+\n+Similarly[^\n]+\n+)(.+?)(\n\n## Batch)', re.DOTALL)
        
        # Update real-time.md Python section
        real_time_content = realtime_python_section_regex.sub(
            f'\\1{realtime_python_section}\\3', 
            real_time_content
        )
        
        # Update real-time.md CLI section
        real_time_content = realtime_cli_section_regex.sub(
            f'\\1{realtime_bash_section}\\3', 
            real_time_content
        )
        
        # Update batch.md Python section
        batch_content = batch_python_section_regex.sub(
            f'\\1{batch_python_section}\\3', 
            batch_content
        )
        
        # Update batch.md CLI section
        batch_content = batch_cli_section_regex.sub(
            f'\\1{batch_bash_section}\\3', 
            batch_content
        )
        
        # Write updated content back to files
        with open(REALTIME_MD, 'w', encoding='utf-8') as f:
            f.write(real_time_content)
        
        with open(BATCH_MD, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        print(f"✓ Added {len(sorted_models)} models to documentation (alphabetically sorted)")
        return True
        
    except Exception as e:
        print(f"✗ Error rebuilding documentation: {e}")
        import traceback
        traceback.print_exc()
        return False
