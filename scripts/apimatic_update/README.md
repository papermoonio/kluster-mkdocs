# Kluster OpenAPI 

This project contains tools to download and prepare the Kluster.ai API specification for import into APIMATIC.

## Overview

The Kluster.ai API requires some modifications to its OpenAPI specification before it can be imported into APIMATIC. This project provides scripts to:

1. Download the latest API specification from Kluster.ai
2. Process the specification to make it compatible with APIMATIC

## File Structure

- `main.py` - Simplified script that processes the OpenAPI specification
- `get_api_specs.py` - Downloads the latest API specification from Kluster.ai
- `kluster_openapi.json` - The downloaded OpenAPI specification
- `kluster_openapi_fixed.json` - The processed OpenAPI specification ready for APIMATIC import

## Requirements

- Python 3.6 or higher
- `requests` library for API calls

## Usage Instructions

### 1. Download the API Specification

```bash
python get_kluster_api.py
```

This script will:
- Prompt you for your Kluster.ai API key
- Download the latest API specification from Kluster.ai
- Save it to `kluster_openapi.json`

### 2. Process the API Specification for APIMATIC

```bash
python fix_api.py [input_file] [output_file]
```

Parameters:
- `input_file` (optional): Path to the input OpenAPI specification (defaults to `kluster_openapi.json`)
- `output_file` (optional): Path to save the processed specification (defaults to `kluster_openapi_fixed.json`)

This script addresses common APIMATIC warnings including:
- "Model has no fields which is not allowed" (LogitBias)
- "Invalid sample value has been removed" (data arrays and Message5)
- Missing array brackets in examples
- Missing content-type specifications

This script will:
- Update server URLs from platform.kluster.ai to api.kluster.ai
- Add OAuth authentication configuration alongside the existing API key auth
- Fix structural issues in the specification for compatibility with APIMATIC
- Save the processed specification to the output file

## Modifications Made to the API Specification

The `main.py` script makes the following essential modifications without hardcoded fixes:

1. **Server URL Update**: 
   - Changes all instances of `platform.kluster.ai` to `api.kluster.ai`

2. **Authentication Configuration**:
   - Replaces OAuth with HTTP Bearer Authentication to match APIMATIC expectations
   - Sets up appropriate security requirements at the global level

3. **Examples Addition**:
   - Adds examples to the completions endpoint for better documentation

4. **Basic Structural Fixes**:
   - Ensures all schema objects with properties have a defined type
   - Fixes array examples with missing brackets

