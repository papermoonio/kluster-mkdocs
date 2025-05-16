"""
API interaction functions for the generate_snippets module.
"""

import requests
from typing import Dict, List, Any

def fetch_models_from_api() -> List[Dict[str, Any]]:
    """Fetch models from the kluster.ai API."""
    try:
        response = requests.get(
            'https://api.kluster.ai/v1/models?extended=true',
            headers={'Accept': 'application/json'}
        )
        response.raise_for_status()
        return response.json()["data"]
    except Exception as e:
        print(f"Error fetching models from API: {e}")
        raise
