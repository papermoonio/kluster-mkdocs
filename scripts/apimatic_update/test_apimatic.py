#!/usr/bin/env python3
"""
APImatic Error Checker 

Tests OpenAPI spec against known APImatic compatibility issues.
Usage: python test_apimatic.py [spec_file]
"""

import json
import sys

def scan_object(obj, checks, path=""):
    """Recursively scan object with multiple check functions"""
    results = []
    
    if isinstance(obj, dict):
        for check in checks:
            results.extend(check(obj, path))
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                results.extend(scan_object(value, checks, f"{path}.{key}"))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, (dict, list)):
                results.extend(scan_object(item, checks, f"{path}[{i}]"))
    
    return results

def check_array_examples(obj, path):
    """Check for array fields with non-array examples"""
    if (obj.get('type') == 'array' and 'example' in obj and 
        not isinstance(obj['example'], list) and obj['example'] is not None):
        return [('error', path, f"Array has non-array example", "Missing bracket(s) for an array")]
    return []

def check_empty_objects(obj, path):
    """Check for empty object schemas"""
    if (obj.get('type') == 'object' and not obj.get('properties') and 
        not obj.get('additionalProperties') and 'schemas' in path):
        return [('error', path, "Empty object schema", "Model has no fields which is not allowed")]
    return []

def check_data_arrays(obj, path):
    """Check for inline schemas in data arrays"""
    if (path.endswith('.data') and obj.get('type') == 'array' and 'items' in obj and
        isinstance(obj['items'], dict) and obj['items'].get('type') == 'object' and
        'properties' in obj['items']):
        return [('info', path, f"Inline schema in data array", "Will become Datum schema")]
    return []

def check_anyof_enums(obj, path):
    """Check for anyOf enum structures"""
    if 'anyOf' in obj and isinstance(obj['anyOf'], list):
        # Simple enum anyOf pattern
        if all(isinstance(item, dict) and 'enum' in item and len(item.get('enum', [])) == 1 
               for item in obj['anyOf']):
            return [('info', path, f"anyOf enum with {len(obj['anyOf'])} values", "Could be simplified")]
    return []

def test_apimatic_compatibility(spec_path):
    """Main test function"""
    print(f"=== APIMATIC COMPATIBILITY TEST ===")
    print(f"Testing: {spec_path}\n")
    
    try:
        with open(spec_path, 'r') as f:
            spec = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error: {e}")
        return
    
    issues = []
    
    # 1. Run object scans
    checks = [check_array_examples, check_empty_objects, check_data_arrays, check_anyof_enums]
    issues.extend(scan_object(spec, checks))
    
    # 2. Specific checks
    
    # Server URL check
    for i, server in enumerate(spec.get('servers', [])):
        if 'platform.kluster.ai' in server.get('url', ''):
            issues.append(('error', f'servers[{i}]', f"Wrong server URL: {server['url']}", "Should use api.kluster.ai"))
    
    # Auth check
    schemes = spec.get('components', {}).get('securitySchemes', {})
    if 'bearerAuth' not in schemes:
        issues.append(('warning', 'auth', "Missing bearerAuth", "No bearer authentication configured"))
    
    # Naming check
    naming_count = count_in_object(spec, lambda s: "Kluster AI" in s if isinstance(s, str) else False)
    if naming_count:
        issues.append(('style', 'naming', f"{naming_count} instances of 'Kluster AI'", "Should be 'kluster.ai'"))
    
    # Message anyOf check
    chat_path = spec.get('paths', {}).get('/v1/chat/completions', {}).get('post', {})
    messages_items = (chat_path.get('requestBody', {})
                     .get('content', {}).get('application/json', {})
                     .get('schema', {}).get('properties', {})
                     .get('messages', {}).get('items', {}))
    
    if 'anyOf' in messages_items:
        if 'example' in messages_items:
            issues.append(('error', 'chat.messages', "Example conflicts with anyOf", "Message5 role enum error"))
        issues.append(('warning', 'chat.messages', "anyOf structure", "Will create Message1-5 schemas"))
    
    # 3. Results
    errors = [i for i in issues if i[0] == 'error']
    warnings = [i for i in issues if i[0] in ['warning', 'info', 'style']]
    data_schemas = len([i for i in issues if 'data array' in i[2]])
    
    print(f"❌ ERRORS: {len(errors)}")
    print(f"⚠️  WARNINGS: {len(warnings)}")
    print(f"📊 DATA SCHEMAS: {data_schemas}")
    
    if errors:
        print(f"\n❌ Critical errors:")
        for _, location, issue, msg in errors:
            print(f"  🚨 {location}: {issue}")
            print(f"     APImatic: {msg}")
    else:
        print("\n✅ No critical errors found!")
    
    if warnings:
        print(f"\n⚠️  Warnings:")
        for _, location, issue, msg in warnings[:3]:  # Show first 3
            print(f"  ⚠️  {location}: {issue}")
    
    print(f"\n📋 SUMMARY: {len(errors)} errors, {len(warnings)} warnings")
    if len(errors) == 0:
        print("   Spec should work well with APImatic!")

def count_in_object(obj, predicate):
    """Count items in nested object matching predicate"""
    count = 0
    if predicate(obj):
        count += 1
    elif isinstance(obj, dict):
        for value in obj.values():
            count += count_in_object(value, predicate)
    elif isinstance(obj, list):
        for item in obj:
            count += count_in_object(item, predicate)
    return count

def main():
    spec_path = sys.argv[1] if len(sys.argv) > 1 else "kluster_openapi.json"
    test_apimatic_compatibility(spec_path)

if __name__ == "__main__":
    main()