#!/usr/bin/env python3
"""
Kluster API Specification Fixer for APIMATIC

Fixes critical compatibility issues:
1. Server URL: platform.kluster.ai → api.kluster.ai
2. Authentication: Adds HTTP Bearer auth
3. Enum expansion: Converts anyOf enums to simple arrays
4. Empty models: Fixes models with no fields

Usage:
  python fix_api.py [input_file] [output_file]
"""

import sys
import json
import os

def fix_anyof_enums(spec):
    """Convert anyOf enum structures to simple enum arrays."""
    enums_fixed = 0
    
    def process_schema(schema):
        nonlocal enums_fixed
        
        if not isinstance(schema, dict):
            return
        
        # Fix anyOf enums
        if 'anyOf' in schema and isinstance(schema['anyOf'], list):
            all_enums = True
            enum_values = []
            enum_type = None
            
            for item in schema['anyOf']:
                if isinstance(item, dict) and 'enum' in item and 'type' in item:
                    if isinstance(item['enum'], list) and len(item['enum']) == 1:
                        enum_values.append(item['enum'][0])
                        if enum_type is None:
                            enum_type = item['type']
                    else:
                        all_enums = False
                        break
                else:
                    all_enums = False
                    break
            
            if all_enums and enum_values and enum_type:
                del schema['anyOf']
                schema['type'] = enum_type
                schema['enum'] = enum_values
                enums_fixed += 1
        
        # Recursively process nested schemas
        for key in list(schema.keys()):
            if key in ['properties', 'items', 'allOf', 'oneOf', 'anyOf']:
                if key == 'properties' and isinstance(schema[key], dict):
                    for prop in schema[key].values():
                        process_schema(prop)
                elif key == 'items':
                    process_schema(schema[key])
                elif isinstance(schema[key], list):
                    for item in schema[key]:
                        process_schema(item)
    
    # Process all schemas
    if 'components' in spec and 'schemas' in spec['components']:
        for schema in spec['components']['schemas'].values():
            process_schema(schema)
    
    # Process all paths
    for path_item in spec.get('paths', {}).values():
        for operation in path_item.values():
            if not isinstance(operation, dict):
                continue
            
            # Process parameters
            for param in operation.get('parameters', []):
                if 'schema' in param:
                    process_schema(param['schema'])
            
            # Process request/response bodies
            for content in ['requestBody', 'responses']:
                if content in operation:
                    if content == 'requestBody' and 'content' in operation[content]:
                        for media_type in operation[content]['content'].values():
                            if 'schema' in media_type:
                                process_schema(media_type['schema'])
                    elif content == 'responses':
                        for response in operation[content].values():
                            if 'content' in response:
                                for media_type in response['content'].values():
                                    if 'schema' in media_type:
                                        process_schema(media_type['schema'])
    
    return enums_fixed

def fix_empty_models(spec):
    """Fix models that have no fields."""
    models_fixed = 0
    
    if 'components' in spec and 'schemas' in spec.get('components', {}):
        for schema_name, schema in spec['components']['schemas'].items():
            if isinstance(schema, dict):
                # Check if it's an empty object
                if schema.get('type') == 'object' and not schema.get('properties'):
                    if schema_name == 'LogitBias':
                        # LogitBias is a map of token IDs to bias values
                        spec['components']['schemas'][schema_name] = {
                            "type": "object",
                            "description": "Modify the likelihood of tokens appearing in the completion",
                            "additionalProperties": {
                                "type": "number",
                                "minimum": -100,
                                "maximum": 100
                            }
                        }
                        models_fixed += 1
    
    return models_fixed

def main():
    # Parse arguments
    if len(sys.argv) > 2:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
    elif len(sys.argv) > 1:
        input_path = sys.argv[1]
        output_path = "kluster_openapi_fixed.json"
    else:
        input_path = "kluster_openapi.json"
        output_path = "kluster_openapi_fixed.json"
    
    # Check input file
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found")
        sys.exit(1)
    
    print(f"Processing: {input_path} → {output_path}\n")
    
    # Load spec
    with open(input_path, 'r') as f:
        spec = json.load(f)
    
    # 1. Fix server URL
    if 'servers' in spec:
        for server in spec['servers']:
            if 'url' in server and 'platform.kluster.ai' in server['url']:
                server['url'] = server['url'].replace('platform.kluster.ai', 'api.kluster.ai')
                print(f"✓ Updated server URL to {server['url']}")
    
    # 2. Fix authentication
    if 'components' in spec and 'securitySchemes' in spec['components']:
        spec['components']['securitySchemes'] = {
            'bearerAuth': {
                'type': 'http',
                'scheme': 'bearer'
            }
        }
        spec['security'] = [{'bearerAuth': []}]
        print("✓ Added Bearer authentication")
    
    # 3. Fix anyOf enums
    enums_fixed = fix_anyof_enums(spec)
    if enums_fixed > 0:
        print(f"✓ Fixed {enums_fixed} anyOf enum structures")
    
    # 4. Fix empty models
    models_fixed = fix_empty_models(spec)
    if models_fixed > 0:
        print(f"✓ Fixed {models_fixed} empty models")
    
    # Save output
    with open(output_path, 'w') as f:
        json.dump(spec, f, indent=2)
    
    print(f"\n✅ Saved to {output_path}")
    print("\nNote: APIMATIC may show multiple message tabs for anyOf schemas - this is their default UI behavior.")

if __name__ == "__main__":
    main()