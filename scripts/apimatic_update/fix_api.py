#!/usr/bin/env python3
"""
Kluster API Specification Cleaner

This script prepares OpenAPI specifications from Kluster.ai for APIMATIC import by:
1. Updating the server URL from platform.kluster.ai to api.kluster.ai
2. Adding HTTP Bearer Authentication (matching APIMATIC's implementation)
3. Adding examples to the completions endpoint
4. Basic structural fixes for OpenAPI compatibility

Usage:
  python main.py [input_file] [output_file]
"""

import sys
import json
import os
import copy

def fix_openapi_spec(input_path, output_path):
    """
    Fix an OpenAPI specification for APIMATIC import.<
    
    Args:
        input_path: Path to the input OpenAPI spec file (JSON)
        output_path: Path where the fixed OpenAPI spec will be saved
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Load the OpenAPI spec
        with open(input_path, 'r') as f:
            spec = json.load(f)
        
        # Keep a copy of the original spec for comparison
        original_spec = copy.deepcopy(spec)
        
        # 1. Fix server URLs - change platform.kluster.ai to api.kluster.ai
        if 'servers' in spec:
            for server in spec['servers']:
                if 'url' in server and 'platform.kluster.ai' in server['url']:
                    server['url'] = server['url'].replace('platform.kluster.ai', 'api.kluster.ai')
                    print(f"✓ Changed server URL to {server['url']}")
        
        # 2. Add Bearer Auth security scheme (matching APIMATIC version)
        if 'components' in spec and 'securitySchemes' in spec['components']:
            # Replace with HTTP Bearer Authentication
            spec['components']['securitySchemes'] = {
                'bearerAuth': {
                    'type': 'http',
                    'scheme': 'bearer'
                }
            }
            print("✓ Added HTTP Bearer Authentication scheme")
            
            # Add security requirement at the root level
            spec['security'] = [
                {'bearerAuth': []}
            ]
            print("✓ Added global security requirements")
        
        # 3. Add examples for completions endpoint
        completions_enhanced = False
        
        for path, methods in spec.get('paths', {}).items():
            # Check if this is the completions endpoint
            is_completions_endpoint = '/v1/chat/completions' in path
            
            for method, operation in methods.items():
                if not is_completions_endpoint or method != 'post':
                    continue
                
                # Add specific examples for the completions endpoint
                if 'requestBody' in operation and 'content' in operation['requestBody']:
                    operation['requestBody']['content']['application/json']['example'] = {
                        "stream": False,
                        "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
                        "messages": [
                            {
                                "role": "user",
                                "content": "Create the ultimate breakfast sandwich."
                            }
                        ],
                        "session_id": "Hew3PY-DtxzQEj1HA-Cu",
                        "chat_id": "886713bb-b319-40ad-9f42-be79f4a4f699",
                        "id": "e42a494c-0f39-48f5-89d7-cee39972c219"
                    }
                    
                    # Add operationId for better code generation
                    operation['operationId'] = "V1ChatCompletions_POST"
                    completions_enhanced = True
                    print("✓ Added examples to completions endpoint")
                    
                    # Add example response
                    for status_code, response in operation.get('responses', {}).items():
                        if status_code == '200' and 'content' in response:
                            response['content']['application/json']['example'] = {
                                "id": "chatcmpl-123456789",
                                "object": "chat.completion",
                                "created": 1677858242,
                                "model": "gpt-3.5-turbo",
                                "choices": [
                                    {
                                        "message": {
                                            "role": "assistant",
                                            "content": "Hello! Yes, I'd be happy to help you today. What do you need assistance with?"
                                        },
                                        "index": 0,
                                        "finish_reason": "stop"
                                    }
                                ],
                                "usage": {
                                    "prompt_tokens": 23,
                                    "completion_tokens": 17,
                                    "total_tokens": 40
                                }
                            }
        
        # 4. Basic structural fixes (minimal and non-destructive)
        
        # Fix schemas that have properties but no type
        schemas_fixed = 0
        
        if 'components' in spec and 'schemas' in spec.get('components', {}):
            for schema_name, schema in spec['components']['schemas'].items():
                if 'properties' in schema and 'type' not in schema:
                    schema['type'] = 'object'
                    schemas_fixed += 1
        
        if schemas_fixed > 0:
            print(f"✓ Fixed {schemas_fixed} schema(s) missing type")
        
        # Simple fix for array examples that are provided as strings
        array_examples_fixed = 0
        
        # Helper function to fix array examples (simplified)
        def fix_array_examples(obj, parent_key=None):
            nonlocal array_examples_fixed
            
            if isinstance(obj, dict):
                for key, value in list(obj.items()):
                    # Check if this is a property that should be an array but has string example
                    if key == 'example' and parent_key in ['errors', 'labels', 'tags'] and isinstance(value, str):
                        # Convert string example to array example
                        obj[key] = [value]
                        array_examples_fixed += 1
                    elif isinstance(value, (dict, list)):
                        # Recursively process nested structures
                        fix_array_examples(value, key)
            elif isinstance(obj, list):
                for item in obj:
                    if isinstance(item, (dict, list)):
                        fix_array_examples(item)
        
        # Process the entire spec to fix array examples
        fix_array_examples(spec)
        
        if array_examples_fixed > 0:
            print(f"✓ Fixed {array_examples_fixed} array examples with missing brackets")
        
        # 5. Save the fixed spec
        with open(output_path, 'w') as f:
            json.dump(spec, f, indent=2)
        
        print(f"\nFixed OpenAPI specification saved to: {output_path}")
        
        # Report changes made
        if spec == original_spec:
            print("No changes were made to the specification.")
        else:
            print("Changes successfully applied to the specification.")
        
        return True
    
    except Exception as e:
        print(f"Error fixing OpenAPI specification: {e}")
        return False

def main():
    """Main entry point for the script."""
    # Get input and output file paths
    if len(sys.argv) > 2:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
    elif len(sys.argv) > 1:
        input_path = sys.argv[1]
        output_path = "fixed_" + os.path.basename(input_path)
    else:
        input_path = "kluster_openapi.json"
        output_path = "kluster_openapi_fixed.json"
    
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found")
        print(f"Hint: Run 'python get_api_specs.py' first to download the latest API specification")
        sys.exit(1)
    
    print(f"Processing OpenAPI specification: {input_path} → {output_path}\n")
    
    # Fix the OpenAPI spec
    success = fix_openapi_spec(input_path, output_path)
    
    if success:
        # Provide guidance for APIMATIC import
        print("\nNext steps for APIMATIC import:")
        print("1. Log in to your APIMATIC account")
        print("2. Create a new API or update an existing API")
        print("3. Import the fixed OpenAPI specification")
        print("4. If import fails, check the error message for any remaining issues")
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
