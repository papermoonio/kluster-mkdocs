"""
Model data structures and transformations.
"""

import re
from typing import Dict, List, Any

def convert_to_slug(model_id: str, display_name: str) -> str:
    """Convert a model ID to a filename-friendly slug using the model_id component for consistency."""
    # Extract the model name portion from the ID
    model_part = model_id.split('/')[-1]
    # Lowercase and replace non-alphanumeric characters with hyphens
    slug = model_part.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    # Remove duplicate hyphens and trim hyphens
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug

def get_model_info(models: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract relevant model information from API response."""
    # Filter out embeddings models
    llm_models = [m for m in models if m.get("model_purpose") != "embeddings"]
    
    result = []
    seen_ids = set()  # Track model IDs we've already processed
    seen_slugs = set()  # Track slugs we've already generated
    
    for model in llm_models:
        # Get model ID and display name
        model_id = model["id"]
        
        # Skip duplicate model IDs
        if model_id in seen_ids:
            print(f"⚠️ Warning: Skipping duplicate model ID: {model_id}")
            continue
        seen_ids.add(model_id)
        
        display_name = model.get("name", model_id.split('/')[-1])
        
        # Clean up display name if derived from ID
        if "name" not in model:
            display_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', display_name)
            display_name = display_name.replace('-', ' ').replace('_', ' ')
        
        # Check for vision capabilities
        supports_vision = (model.get("model_purpose") == "multimodal" or 
                          "vision" in model.get("tags", []))
        
        # Get file slug using our improved function
        file_slug = convert_to_slug(model_id, display_name)
        
        # Handle duplicate slugs by adding a numeric suffix
        base_slug = file_slug
        counter = 1
        while file_slug in seen_slugs:
            file_slug = f"{base_slug}-{counter}"
            counter += 1
            print(f"⚠️ Warning: Found duplicate slug. Changed {base_slug} to {file_slug}")
        seen_slugs.add(file_slug)
        
        result.append({
            "id": model_id,
            "display_name": display_name,
            "file_slug": file_slug,
            "supports_vision": supports_vision
        })
    
    return result
