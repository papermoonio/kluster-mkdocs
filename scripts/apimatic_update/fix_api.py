#!/usr/bin/env python3
"""
Kluster API Specification Fixer for APIMATIC.

Fixes all critical compatibility issues in one pass.
Usage: python fix_api.py [input_file] [output_file]
"""

import sys
import json
import os

def apply_fixes(obj, fixes, path=""):
    """Apply multiple fix functions to object recursively"""
    fixed_count = 0
    
    if isinstance(obj, dict):
        # Apply all fixes to current object
        for fix in fixes:
            fixed_count += fix(obj, path)
        
        # Recurse into nested objects
        for key, value in list(obj.items()):
            if isinstance(value, (dict, list)):
                fixed_count += apply_fixes(value, fixes, f"{path}.{key}")
    
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, (dict, list)):
                fixed_count += apply_fixes(item, fixes, f"{path}[{i}]")
    
    return fixed_count

def fix_array_examples(obj, path):
    """Fix array examples that are not in array format"""
    if obj.get('type') == 'array' and 'example' in obj:
        if not isinstance(obj['example'], list) and obj['example'] is not None:
            obj['example'] = [obj['example']]
            return 1
    return 0

def fix_anyof_enums(obj, path):
    """Convert anyOf enum structures to simple enum arrays"""
    if 'anyOf' in obj and isinstance(obj['anyOf'], list):
        # Check if all items are simple single-value enums
        enum_values = []
        enum_type = None
        
        for item in obj['anyOf']:
            if (isinstance(item, dict) and 'enum' in item and 'type' in item and
                isinstance(item['enum'], list) and len(item['enum']) == 1):
                enum_values.append(item['enum'][0])
                if enum_type is None:
                    enum_type = item['type']
            else:
                return 0  # Not a simple enum anyOf
        
        if enum_values and enum_type:
            del obj['anyOf']
            obj['type'] = enum_type
            obj['enum'] = enum_values
            return 1
    return 0

def fix_naming(obj, path):
    """Fix 'Kluster AI' to 'kluster.ai' naming"""
    count = 0
    for key, value in list(obj.items()):
        if isinstance(value, str):
            if "Kluster AI" in value or "KLUSTER AI" in value:
                obj[key] = value.replace("Kluster AI", "kluster.ai").replace("KLUSTER AI", "kluster.ai")
                count += 1
    return count

def main():
    # Parse arguments
    if len(sys.argv) > 2:
        input_path, output_path = sys.argv[1], sys.argv[2]
    elif len(sys.argv) > 1:
        input_path, output_path = sys.argv[1], "kluster_openapi_fixed.json"
    else:
        input_path, output_path = "kluster_openapi.json", "kluster_openapi_fixed.json"
    
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
    if 'components' not in spec:
        spec['components'] = {}
    spec['components']['securitySchemes'] = {
        'bearerAuth': {'type': 'http', 'scheme': 'bearer'}
    }
    spec['security'] = [{'bearerAuth': []}]
    print("✓ Added Bearer authentication")
    
    # 3. Fix empty LogitBias model
    if ('components' in spec and 'schemas' in spec['components'] and 
        'LogitBias' in spec['components']['schemas']):
        logit_bias = spec['components']['schemas']['LogitBias']
        if logit_bias.get('type') == 'object' and not logit_bias.get('properties'):
            spec['components']['schemas']['LogitBias'] = {
                "type": "object",
                "description": "Modify the likelihood of tokens appearing in the completion",
                "additionalProperties": {
                    "type": "number",
                    "minimum": -100,
                    "maximum": 100
                }
            }
            print("✓ Fixed LogitBias empty model")
    
    # 4. Flatten message anyOf structure
    chat_path = '/v1/chat/completions'
    if chat_path in spec.get('paths', {}):
        post = spec['paths'][chat_path].get('post', {})
        messages_schema = (post.get('requestBody', {})
                          .get('content', {}).get('application/json', {})
                          .get('schema', {}).get('properties', {})
                          .get('messages', {}))
        
        if 'items' in messages_schema and 'anyOf' in messages_schema['items']:
            items = messages_schema['items']
            variants = items['anyOf']
            
            # Collect all properties and role enums
            all_properties = {}
            all_role_enums = set()
            all_required = set()
            
            for variant in variants:
                if isinstance(variant, dict) and 'properties' in variant:
                    for prop_name, prop_def in variant['properties'].items():
                        if prop_name == 'role' and 'enum' in prop_def:
                            all_role_enums.update(prop_def['enum'])
                        else:
                            if prop_name not in all_properties:
                                all_properties[prop_name] = prop_def.copy()
                    
                    if 'required' in variant:
                        all_required.update(variant['required'])
            
            # Create unified schema
            if all_role_enums:
                all_properties['role'] = {
                    'type': 'string',
                    'enum': sorted(list(all_role_enums)),
                    'description': 'Role of the message sender.'
                }
            
            # Remove example at items level if it exists
            if 'example' in items:
                del items['example']
            
            # Replace anyOf with unified schema
            items.clear()
            items.update({
                'type': 'object',
                'description': items.get('description', 'Chat completion message.'),
                'properties': all_properties
            })
            
            if all_required:
                items['required'] = sorted(list(all_required))
            
            print("✓ Flattened message anyOf structure")
    
    # 5. Apply recursive fixes
    fixes = [fix_array_examples, fix_anyof_enums, fix_naming]
    total_fixes = apply_fixes(spec, fixes)
    
    # Count and report individual fixes
    array_fixes = apply_fixes(spec, [lambda o, p: 0], "")  # Already applied above
    enum_fixes = total_fixes  # Approximation
    naming_fixes = 0  # Already applied above
    
    print(f"✓ Fixed array examples and other issues")
    
    # Save output
    with open(output_path, 'w') as f:
        json.dump(spec, f, indent=2)
    
    print(f"\n✅ Saved to {output_path}")
    print("Note: APIMATIC may show multiple message tabs for anyOf schemas - this is their default UI behavior.")

if __name__ == "__main__":
    main()