# Model Onboarding Documentation for kluster.ai Platform

## Overview

This document details the complete process for onboarding a new model to the kluster.ai platform documentation. It covers all necessary file locations, required changes, and integration steps to ensure the model is properly accessible through both real-time and batch inference examples.

## File Structure

When onboarding a new model, we need to create or modify files in the following directories:

```
/Users/franzuzz/code/kluster-mkdocs/kluster-docs/.snippets/code/get-started/start-building/
├── batch/
│   ├── batch-jsonl-{model-name}.md      # Bash example for batch inference
│   └── batch-jsonl-{model-name}.py      # Python example for batch inference
└── real-time/
    ├── real-time-{model-name}.md        # Bash example for real-time inference
    └── real-time-{model-name}.py        # Python example for real-time inference
```

Additionally, we need to update the following Markdown files to include the new model in the documentation:

```
/Users/franzuzz/code/kluster-mkdocs/kluster-docs/get-started/start-building/
├── batch.md       # Documentation for batch inference 
└── real-time.md   # Documentation for real-time inference
```

## Step 1: Create Example Files

### 1.1. Create Real-Time Examples

For real-time inference, we need to create two files:

#### 1.1.1. Python Example (`real-time-{model-name}.py`)

This file should contain a complete Python script that demonstrates how to use the model with the OpenAI Python client. The key components include:

- Import necessary libraries (`openai`, `getpass`)
- Initialize the OpenAI client with the kluster.ai base URL
- Create a chat completion request with the specific model ID
- Process and display the response

Example template:
```python
# filepath: /Users/franzuzz/code/kluster-mkdocs/kluster-docs/.snippets/code/get-started/start-building/real-time/real-time-{model-name}.py
from openai import OpenAI
from getpass import getpass

# Get API key from user input
api_key = getpass("Enter your kluster.ai API key: ")

# Initialize OpenAI client pointing to kluster.ai API
client = OpenAI(
    api_key=api_key,
    base_url="https://api.kluster.ai/v1"
)

# Create chat completion request
completion = client.chat.completions.create(
    model="{full-model-id}",
    messages=[
        {"role": "user", "content": "What is the ultimate breakfast sandwich?"}
    ]
)

"""Logs the full AI response to terminal."""

# Extract model name and AI-generated text
model_name = completion.model  
text_response = completion.choices[0].message.content  

# Print response to console
print(f"\n🔍 AI response (model: {model_name}):")
print(text_response)
```

#### 1.1.2. Bash Example (`real-time-{model-name}.md`)

This file contains a bash/curl example for real-time inference:

```markdown
<!-- filepath: /Users/franzuzz/code/kluster-mkdocs/kluster-docs/.snippets/code/get-started/start-building/real-time/real-time-{model-name}.md -->
#!/bin/bash

# Check if API_KEY is set and not empty
if [[ -z "$API_KEY" ]]; then
    echo -e "\nError: API_KEY environment variable is not set.\n" >&2
fi

# Submit real-time request
curl https://api.kluster.ai/v1/chat/completions \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
            \"model\": \"{full-model-id}\", 
            \"messages\": [
                { 
                    \"role\": \"user\", 
                    \"content\": \"What is the ultimate breakfast sandwich?\"
                }
            ]
        }"
```

### 1.2. Create Batch Inference Examples

For batch inference, we need to create two files:

#### 1.2.1. Python Example (`batch-jsonl-{model-name}.py`)

This file should contain a complete Python script demonstrating how to:
- Create batch requests in JSONL format
- Upload the batch file
- Submit the batch job
- Monitor job progress
- Retrieve results

Example template:
```python
# filepath: /Users/franzuzz/code/kluster-mkdocs/kluster-docs/.snippets/code/get-started/start-building/batch/batch-jsonl-{model-name}.py
from openai import OpenAI
from getpass import getpass
import json
import time

# Get API key from user input
api_key = getpass("Enter your kluster.ai API key: ")

# Initialize OpenAI client pointing to kluster.ai API
client = OpenAI(
    base_url="https://api.kluster.ai/v1",
    api_key=api_key,
)

# Create request with specified structure
requests = [
    {
        "custom_id": "request-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "{full-model-id}",
            "messages": [
                {"role": "system", "content": "You are an experienced cook."},
                {"role": "user", "content": "What is the ultimate breakfast sandwich?"},
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-2",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "{full-model-id}",
            "messages": [
                {"role": "system", "content": "You are a maths tutor."},
                {"role": "user", "content": "Explain the Pythagorean theorem."},
            ],
            "max_completion_tokens": 1000,
        },
    },
    {
        "custom_id": "request-4",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "{full-model-id}",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a multilingual, experienced maths tutor.",
                },
                {
                    "role": "user",
                    "content": "Explain the Pythagorean theorem in Spanish",
                },
            ],
            "max_completion_tokens": 1000,
        },
    },
    # Additional tasks can be added here
]

# Save tasks to a JSONL file (newline-delimited JSON)
file_name = "my_batch_request.jsonl"
with open(file_name, "w") as file:
    for request in requests:
        file.write(json.dumps(request) + "\n")

# Upload batch job file
batch_input_file = client.files.create(
        file=open(file_name, "rb"),
        purpose="batch"
)

# Submit batch job
batch_request = client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
)

# Poll the batch status until it's complete
while True:
    batch_status = client.batches.retrieve(batch_request.id)
    print("Batch status: {}".format(batch_status.status))
    print(
        f"Completed tasks: {batch_status.request_counts.completed} / {batch_status.request_counts.total}"
    )

    if batch_status.status.lower() in ["completed", "failed", "cancelled"]:
        break

    time.sleep(10)  # Wait for 10 seconds before checking again

# Check if the Batch completed successfully
if batch_status.status.lower() == "completed":
    # Retrieve the results and log
    result_file_id = batch_status.output_file_id
    results = client.files.content(result_file_id).content

    # Print response to console
    print(f"\n🔍 AI batch response:")
    print(results)
else:
    print(f"Batch failed with status: {batch_status.status}")
```

#### 1.2.2. Bash Example (`batch-jsonl-{model-name}.md`)

This file contains a bash/curl example for batch inference:

```markdown
<!-- filepath: /Users/franzuzz/code/kluster-mkdocs/kluster-docs/.snippets/code/get-started/start-building/batch/batch-jsonl-{model-name}.md -->
#!/bin/bash

# Check if API_KEY is set and not empty
if [[ -z "$API_KEY" ]]; then
    echo "Error: API_KEY environment variable is not set." >&2
fi

# Create request with specified structure
cat << EOF > my_batch_request.jsonl
{"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "{full-model-id}", "messages": [{"role": "system", "content": "You are an experienced cook."}, {"role": "user", "content": "What is the ultimate breakfast sandwich?"}],"max_completion_tokens":1000}}
{"custom_id": "request-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "{full-model-id}", "messages": [{"role": "system", "content": "You are an experienced maths tutor."}, {"role": "user", "content": "Explain the Pythagorean theorem."}],"max_completion_tokens":1000}}
{"custom_id": "request-4", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "{full-model-id}", "messages":[{"role": "system", "content": "You are a multilingual, experienced maths tutor."}, {"role": "user", "content": "Explain the Pythagorean theorem in Spanish"}],"max_completion_tokens":1000}}
EOF

# Upload batch job file
FILE_ID=$(curl -s https://api.kluster.ai/v1/files \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: multipart/form-data" \
    -F "file=@my_batch_request.jsonl" \
    -F "purpose=batch" | jq -r '.id')
echo "File uploaded, file ID: $FILE_ID"

# Submit batch job
BATCH_ID=$(curl -s https://api.kluster.ai/v1/batches \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "input_file_id": "'"$FILE_ID"'",
        "endpoint": "/v1/chat/completions",
        "completion_window": "24h"
    }' | jq -r '.id')
echo "Batch job submitted, job ID: $BATCH_ID"


# Poll the batch status until it's completed
STATUS="in_progress"
while [[ "$STATUS" != "completed" ]]; do
    echo "Waiting for batch job to complete... Status: $STATUS"
    sleep 10 # Wait for 10 seconds before checking again

    STATUS=$(curl -s https://api.kluster.ai/v1/batches/$BATCH_ID \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" | jq -r '.status')
done

# Retrieve the batch output file
KLUSTER_OUTPUT_FILE=$(curl -s https://api.kluster.ai/v1/batches/$BATCH_ID \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" | jq -r '.output_file_id')

# Retrieve the results
OUTPUT_CONTENT=$(curl -s https://api.kluster.ai/v1/files/$KLUSTER_OUTPUT_FILE/content \
    -H "Authorization: Bearer $API_KEY")

# Log results
echo -e "\n🔍 AI batch response:"
echo "$OUTPUT_CONTENT"
```

## Step 2: Update Documentation Files

### 2.1. Update real-time.md

After creating the example files, we need to update the `real-time.md` file to include the new model in both the Python and CLI examples sections.

#### 2.1.1. Add to Python Examples Section

Locate the Python examples section in `real-time.md` and add a new entry for the model:

```markdown
??? example "New Model Name"

    ```python
    --8<-- 'code/get-started/start-building/real-time/real-time-{model-name}.py'
    ```
```

#### 2.1.2. Add to CLI Examples Section

Locate the CLI examples section in `real-time.md` and add a new entry for the model:

```markdown
??? example "New Model Name"

    ```bash
    --8<-- 'code/get-started/start-building/real-time/real-time-{model-name}.md'
    ```
```

### 2.2. Update batch.md

Similarly, we need to update the `batch.md` file to include the new model in both the Python and CLI examples sections.

#### 2.2.1. Add to Python Examples Section

Locate the Python examples section in `batch.md` and add a new entry for the model:

```markdown
??? example "New Model Name"

    ```python
    --8<-- 'code/get-started/start-building/batch/batch-jsonl-{model-name}.py'
    ```
```

#### 2.2.2. Add to CLI Examples Section

Locate the CLI examples section in `batch.md` and add a new entry for the model:

```markdown
??? example "New Model Name"

    ```bash
    --8<-- 'code/get-started/start-building/batch/batch-jsonl-{model-name}.md'
    ```
```

## Naming Conventions

When creating files and references for a new model, follow these conventions:

1. **File naming**: Use lowercase for all filenames, with hyphens separating words
   - For real-time: `real-time-{model-name}.py` and `real-time-{model-name}.md`
   - For batch: `batch-jsonl-{model-name}.py` and `batch-jsonl-{model-name}.md`

2. **Model ID in code**: Always use the exact, case-sensitive model ID (e.g., `mistralai/Mistral-Nemo-Instruct-2407`)

3. **Display name in documentation**: Use the human-readable name with proper capitalization (e.g., `Mistral Nemo Instruct 2407`)

## Critical Considerations

1. **File Path Consistency**: Ensure that all file paths in both the code comments and the documentation references match exactly.

2. **Model ID Accuracy**: The model ID specified in the code must exactly match the official model ID format from the API.

3. **Example Consistency**: Keep the examples consistent with other models – only change the model ID and display name.

4. **File Order**: When adding to the documentation files, maintain alphabetical order or the existing order pattern.

5. **Content Completeness**: Each example must include all necessary steps to run a complete inference job.

## Complete Process Example

Here's the full process I followed to onboard "mistralai/Mistral-Nemo-Instruct-2407":

1. Created four files:
   - `/Users/franzuzz/code/kluster-mkdocs/kluster-docs/.snippets/code/get-started/start-building/real-time/real-time-mistral-nemo-instruct-2407.py`
   - `/Users/franzuzz/code/kluster-mkdocs/kluster-docs/.snippets/code/get-started/start-building/real-time/real-time-mistral-nemo-instruct-2407.md`
   - `/Users/franzuzz/code/kluster-mkdocs/kluster-docs/.snippets/code/get-started/start-building/batch/batch-jsonl-mistral-nemo-instruct-2407.py`
   - `/Users/franzuzz/code/kluster-mkdocs/kluster-docs/.snippets/code/get-started/start-building/batch/batch-jsonl-mistral-nemo-instruct-2407.md`

2. Added the new model to the documentation files:
   - In `/Users/franzuzz/code/kluster-mkdocs/kluster-docs/get-started/start-building/real-time.md`, added:
     ```markdown
     ??? example "Mistral Nemo Instruct 2407"

         ```python
         --8<-- 'code/get-started/start-building/real-time/real-time-mistral-nemo-instruct-2407.py'
         ```
     ```
     and
     ```markdown
     ??? example "Mistral Nemo Instruct 2407"

         ```bash
         --8<-- 'code/get-started/start-building/real-time/real-time-mistral-nemo-instruct-2407.md'
         ```
     ```

   - In `/Users/franzuzz/code/kluster-mkdocs/kluster-docs/get-started/start-building/batch.md`, added:
     ```markdown
     ??? example "Mistral Nemo Instruct 2407"

         ```python
         --8<-- 'code/get-started/start-building/batch/batch-jsonl-mistral-nemo-instruct-2407.py'
         ```
     ```
     and
     ```markdown
     ??? example "Mistral Nemo Instruct 2407"

         ```bash
         --8<-- 'code/get-started/start-building/batch/batch-jsonl-mistral-nemo-instruct-2407.md'
         ```
     ```

## Troubleshooting

### Common Issues

1. **File Already Exists**: If you get an error that a file already exists, use a file modification tool instead of file creation.

2. **Include Path Errors**: If examples aren't showing up in the documentation, check that the file path in the `--8<--` include tag is correct.

3. **Case Sensitivity**: Ensure the model ID matches exactly, including capitalization.

4. **Name Consistency**: Keep the displayed model name consistent across all references.

### Verification Process

Before considering the onboarding complete, verify:

1. All four files exist and have the correct content
2. The model ID is consistent in all examples
3. The model appears in both dropdown sections in both documentation pages
4. The file paths and references all use consistent naming conventions

## Conclusion

Onboarding a new model to the kluster.ai platform documentation involves creating four example files and updating two markdown files to include references to these examples. Following the established patterns and conventions ensures that users can easily find and use the new model in both real-time and batch inference scenarios.

The most critical factors for success are:
1. Exact match of model ID in all code examples
2. Consistent file naming and organization
3. Proper inclusion of examples in documentation files
4. Following the same format and structure as existing model examples

By adhering to these guidelines, you can efficiently onboard new models to the kluster.ai platform documentation.
