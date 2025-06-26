#!/usr/bin/env python3
"""
kluster.ai API Specification Fixer.
Fetches the original API spec from https://api.kluster.ai/v1/admin/openapi.json
and fixes all critical compatibility issues in one pass.
Usage: python process_api_spec.py [output_file]
"""

import re
import sys
import json
import requests

# Abbreviations that should remain fully capitalized in tag names
CAPITALIZED_ABBREVIATIONS = ["MCP"]


def fetch_api_spec(url):
    """Fetch API specification from the given URL"""
    try:
        print(f"Fetching API spec from {url}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching API spec: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        sys.exit(1)


def format_tag_name(tag_name):
    """Format tag name with proper capitalization for abbreviations"""
    # Split on uppercase letters and apply sentence casing
    split_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', tag_name)
    formatted_name = split_name.capitalize()
    
    # Check if the formatted name matches any abbreviations (case-insensitive)
    for abbrev in CAPITALIZED_ABBREVIATIONS:
        if formatted_name.lower() == abbrev.lower():
            return abbrev
    
    return formatted_name


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
    if obj.get("type") == "array" and "example" in obj:
        if not isinstance(obj["example"], list) and obj["example"] is not None:
            obj["example"] = [obj["example"]]
            return 1
    return 0


def fix_anyof_enums(obj, path):
    """Convert anyOf enum structures to simple enum arrays"""
    if "anyOf" in obj and isinstance(obj["anyOf"], list):
        # Check if all items are simple single-value enums
        enum_values = []
        enum_type = None

        for item in obj["anyOf"]:
            if (
                isinstance(item, dict)
                and "enum" in item
                and "type" in item
                and isinstance(item["enum"], list)
                and len(item["enum"]) == 1
            ):
                enum_values.append(item["enum"][0])
                if enum_type is None:
                    enum_type = item["type"]
            else:
                return 0  # Not a simple enum anyOf

        if enum_values and enum_type:
            del obj["anyOf"]
            obj["type"] = enum_type
            obj["enum"] = enum_values
            return 1
    return 0


def fix_naming(obj, path):
    """Fix various Kluster naming variations to 'kluster.ai'"""
    count = 0
    for key, value in list(obj.items()):
        if isinstance(value, str):
            original_value = value
            # Replace all variations of Kluster naming with kluster.ai
            value = re.sub(r'\bKlusterAI\b', 'kluster.ai', value)
            value = re.sub(r'\bKluster AI\b', 'kluster.ai', value)
            value = re.sub(r'\bKLUSTER AI\b', 'kluster.ai', value)
            value = re.sub(r'\bKluster\.ai\b', 'kluster.ai', value)
            value = re.sub(r'\bKLUSTERAI\b', 'kluster.ai', value)
            
            if value != original_value:
                obj[key] = value
                count += 1
    return count


def main():
    # Parse arguments
    api_url = "https://api.kluster.ai/v1/admin/openapi.json"
    
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    else:
        output_path = "spec/kluster_openapi_fixed.json"

    print(f"Processing: {api_url} → {output_path}\n")

    # Fetch spec from API
    spec = fetch_api_spec(api_url)

    # 1. Fix server URL
    if "servers" in spec:
        for server in spec["servers"]:
            if "url" in server and "platform.kluster.ai" in server["url"]:
                server["url"] = server["url"].replace(
                    "platform.kluster.ai", "api.kluster.ai"
                )
                print(f"✓ Updated server URL to {server['url']}")
    
    # 2. Fix title and description
    if "info" in spec:
        if "title" in spec["info"]:
            spec["info"]["title"] = "Get started with the kluster.ai API"
            print("✓ Updated API title to 'kluster.ai'")
        if "description" in spec["info"]:
            spec["info"]["description"] = "The kluster.ai API provides a simple and scalable way to work with Large Language Models (LLMs). It's compatible with OpenAI’s API and SDKs, allowing easy integration into your existing workflows with minimal code changes.\n\nVisit the [Get an API key](https://docs.kluster.ai/get-started/get-api-key/) page to create an account and generate your API key.\n\nTo use the API playground, enter your API key under **Authentication** in the **Bearer token** field on the right side of the page.\n\nYou're now ready to make test API calls. Choose an endpoint and click **Test Request** to send a request. Your API key will be automatically included—just update the parameters as needed and submit.\n\nNote that the API playground does not store your API key between sessions. Be mindful of request limits based on your plan tier when testing."
            print("✓ Updated API description to 'kluster.ai'")

    # 3. Fix authentication
    if "components" not in spec:
        spec["components"] = {}
    spec["components"]["securitySchemes"] = {
        "bearerAuth": {"type": "http", "scheme": "bearer"}
    }
    spec["security"] = [{"bearerAuth": []}]
    print("✓ Added Bearer authentication")

    # 4. Fix empty LogitBias model
    if (
        "components" in spec
        and "schemas" in spec["components"]
        and "LogitBias" in spec["components"]["schemas"]
    ):
        logit_bias = spec["components"]["schemas"]["LogitBias"]
        if logit_bias.get("type") == "object" and not logit_bias.get("properties"):
            spec["components"]["schemas"]["LogitBias"] = {
                "type": "object",
                "description": "Modify the likelihood of tokens appearing in the completion",
                "additionalProperties": {
                    "type": "number",
                    "minimum": -100,
                    "maximum": 100,
                },
            }
            print("✓ Fixed LogitBias empty model")

    # 5. Flatten message anyOf structure
    chat_path = "/v1/chat/completions"
    if chat_path in spec.get("paths", {}):
        post = spec["paths"][chat_path].get("post", {})
        messages_schema = (
            post.get("requestBody", {})
            .get("content", {})
            .get("application/json", {})
            .get("schema", {})
            .get("properties", {})
            .get("messages", {})
        )

        if "items" in messages_schema and "anyOf" in messages_schema["items"]:
            items = messages_schema["items"]
            variants = items["anyOf"]

            # Collect all properties and role enums
            all_properties = {}
            all_role_enums = set()
            all_required = set()

            for variant in variants:
                if isinstance(variant, dict) and "properties" in variant:
                    for prop_name, prop_def in variant["properties"].items():
                        if prop_name == "role" and "enum" in prop_def:
                            all_role_enums.update(prop_def["enum"])
                        else:
                            if prop_name not in all_properties:
                                all_properties[prop_name] = prop_def.copy()

                    if "required" in variant:
                        all_required.update(variant["required"])

            # Create unified schema
            if all_role_enums:
                all_properties["role"] = {
                    "type": "string",
                    "enum": sorted(list(all_role_enums)),
                    "description": "Role of the message sender.",
                }

            # Remove example at items level if it exists
            if "example" in items:
                del items["example"]

            # Replace anyOf with unified schema
            items.clear()
            items.update(
                {
                    "type": "object",
                    "description": items.get("description", "Chat completion message."),
                    "properties": all_properties,
                }
            )

            if all_required:
                items["required"] = sorted(list(all_required))

            print("✓ Flattened message anyOf structure")

    # 6. Apply recursive fixes
    fixes = [fix_array_examples, fix_anyof_enums, fix_naming]
    total_fixes = apply_fixes(spec, fixes)
    
    # Report individual fix counts
    if total_fixes > 0:
        print(f"✓ Applied {total_fixes} recursive fixes (array examples, anyOf enums, naming)")

    # 7. Remove "portal" tags and update tag names
    if "tags" in spec:
        for tag in spec["tags"]:
            if "name" in tag:
                if tag["name"] == "portal":
                    spec["tags"].remove(tag)
                    print("✓ Removed 'portal' tag")
                else:
                    # Update tag name with proper abbreviation handling
                    original_name = tag["name"]
                    new_name = format_tag_name(original_name)
                    tag["name"] = new_name

                    print(f"✓ Updated tag '{original_name}' to '{tag['name']}'")

    # 8. Update endpoint tags throughout the spec
    endpoint_tag_fixes = 0
    if "paths" in spec:
        for path, path_obj in spec["paths"].items():
            for method, method_obj in path_obj.items():
                if isinstance(method_obj, dict) and "tags" in method_obj:
                    if isinstance(method_obj["tags"], list):
                        original_tags = method_obj["tags"].copy()
                        updated_tags = []
                        for tag in method_obj["tags"]:
                            if tag == "portal":
                                # Remove portal tags from endpoints
                                endpoint_tag_fixes += 1
                                continue
                            else:
                                # Format other tags
                                new_tag = format_tag_name(tag)
                                updated_tags.append(new_tag)
                                if new_tag != tag:
                                    endpoint_tag_fixes += 1
                        method_obj["tags"] = updated_tags
    
    if endpoint_tag_fixes > 0:
        print(f"✓ Updated {endpoint_tag_fixes} endpoint tags")

    # 9. Remove undocumented endpoints (those without tags)
    removed_endpoints = []
    if "paths" in spec:
        paths_to_remove = []
        for path, path_obj in spec["paths"].items():
            for method, method_obj in path_obj.items():
                if isinstance(method_obj, dict):
                    # Check if endpoint has no tags or empty tags
                    if "tags" not in method_obj or not method_obj["tags"] or len(method_obj["tags"]) == 0:
                        endpoint_info = f"{method.upper()} {path}"
                        removed_endpoints.append(endpoint_info)
                        # Mark the entire path for removal if all methods are undocumented
                        if path not in paths_to_remove:
                            # Check if any other method in this path has tags
                            has_documented_method = False
                            for other_method, other_method_obj in path_obj.items():
                                if (isinstance(other_method_obj, dict) and 
                                    "tags" in other_method_obj and 
                                    other_method_obj["tags"] and 
                                    len(other_method_obj["tags"]) > 0 and
                                    other_method != method):
                                    has_documented_method = True
                                    break
                            
                            if not has_documented_method:
                                paths_to_remove.append(path)
                            else:
                                # Remove just this method from the path
                                del path_obj[method]
        
        # Remove paths that have no documented methods
        for path in paths_to_remove:
            del spec["paths"][path]
    
    if removed_endpoints:
        print(f"✓ Removed {len(removed_endpoints)} undocumented endpoints")
        for endpoint in removed_endpoints:
            print(f"  ⚠️  Needs to be properly documented: {endpoint}")

    # Save output
    with open(output_path, "w") as f:
        json.dump(spec, f, indent=2)

    print(f"\n✅ Saved to {output_path}")


if __name__ == "__main__":
    main()
