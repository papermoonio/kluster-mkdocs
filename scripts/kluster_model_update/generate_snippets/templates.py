
"""
Template code for code snippets generation.
"""

from typing import Dict, Any

def get_real_time_template(model: Dict[str, Any]) -> str:
    """Return a Python template for real-time API calls."""
    model_id = model["id"]
    model_display_name = model["display_name"]
    template_description = f"Real-time completions with the {model_display_name} model on kluster.ai"
    supports_vision = model.get("supports_vision", False)
    
    # Base template for all models
    template = f'''# {template_description}

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
    model="{model_id}",
    messages=[
        {{"role": "user", "content": "What is the ultimate breakfast sandwich?"}}
    ]
)

"""Logs the full AI response to terminal."""

# Extract model name and AI-generated text
model_name = completion.model
text_response = completion.choices[0].message.content

# Print response to console
print(f"\\n🔍 AI response (model: {{model_name}}):")
print(text_response)
'''
    
    # Add vision-specific template for models that support it
    if supports_vision:
        template = f'''# {template_description}

from openai import OpenAI
from getpass import getpass

image_url = "https://github.com/kluster-ai/klusterai-cookbook/blob/main/images/parking-image.jpeg?raw=true"

# Get API key from user input
api_key = getpass("Enter your kluster.ai API key: ")

# Initialize OpenAI client pointing to kluster.ai API
client = OpenAI(api_key=api_key, base_url="https://api.kluster.ai/v1")

# Create chat completion request
completion = client.chat.completions.create(
    model="{model_id}",
    messages=[
        {{
            "role": "user",
            "content": [
                {{"type": "text", "text": "Who can park in the area?"}},
                {{"type": "image_url", "image_url": {{"url": image_url}}}},
            ],
        }}
    ],
)

print(f"\\nImage URL: {{image_url}}")

"""Logs the full AI response to terminal."""

# Extract model name and AI-generated text
model_name = completion.model
text_response = completion.choices[0].message.content

# Print response to console
print(f"\\n🔍 AI response (model: {{model_name}}):")
print(text_response)
'''
    
    return template

def get_batch_template(model: Dict[str, Any]) -> str:
    """Return a Python template for batch JSONL API calls."""
    model_id = model["id"]
    model_display_name = model["display_name"]
    template_description = f"Batch completions with the {model_display_name} model on kluster.ai"
    supports_vision = model.get("supports_vision", False)
    
    if supports_vision:
        template = f'''# {template_description}
import json
import time
from getpass import getpass

from openai import OpenAI

# Newton's cradle
image1_url="https://github.com/kluster-ai/klusterai-cookbook/blob/main/images/balls-image.jpeg?raw=true"
# Text with typos
image2_url="https://github.com/kluster-ai/klusterai-cookbook/blob/main/images/text-typo-image.jpeg?raw=true"
# Parking sign
image3_url="https://github.com/kluster-ai/klusterai-cookbook/blob/main/images/parking-image.jpeg?raw=true"

# Get API key from user input
api_key = getpass("Enter your kluster.ai API key: ")

# Initialize OpenAI client pointing to kluster.ai API
client = OpenAI(
    base_url="https://api.kluster.ai/v1",
    api_key=api_key,
)

# Create request with specified structure
requests = [
    {{
        "custom_id": "request-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {{
            "model": "{model_id}",
            "messages": [
                {{
                    "role": "user",
                    "content": [
                        {{"type": "text", "text": "What is this?"}},
                        {{
                            "type": "image_url",
                            "image_url": {{
                                "url": image1_url
                            }},
                        }},
                    ],
                }}
            ],
            "max_completion_tokens": 1000,
        }},
    }},
    {{
        "custom_id": "request-2",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {{
            "model": "{model_id}",
            "messages": [
                {{
                    "role": "user",
                    "content": [
                        {{"type": "text", "text": "Extract the text, find typos if any."}},
                        {{
                            "type": "image_url",
                            "image_url": {{
                                "url": image2_url
                            }},
                        }},
                    ],
                }}
            ],
            "max_completion_tokens": 1000,
        }},
    }},
    {{
        "custom_id": "request-3",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {{
            "model": "{model_id}",
            "messages": [
                {{
                    "role": "user",
                    "content": [
                        {{"type": "text", "text": "Who can park in the area?"}},
                        {{
                            "type": "image_url",
                            "image_url": {{
                                "url": image3_url
                            }},
                        }},
                    ],
                }}
            ],
            "max_completion_tokens": 1000,
        }},
    }},
]

# Save tasks to a JSONL file (newline-delimited JSON)
file_name = "my_batch_request.jsonl"
with open(file_name, "w") as file:
    for request in requests:
        file.write(json.dumps(request) + "\\n")

# Upload batch job file
batch_input_file = client.files.create(file=open(file_name, "rb"), purpose="batch")

# Submit batch job
batch_request = client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
)

# Poll the batch status until it's complete
while True:
    batch_status = client.batches.retrieve(batch_request.id)
    print(f"Batch status: {{batch_status.status}}")
    print(
        f"Completed tasks: {{batch_status.request_counts.completed}} / {{batch_status.request_counts.total}}"
    )

    if batch_status.status.lower() in ["completed", "failed", "cancelled"]:
        break

    time.sleep(10)  # Wait for 10 seconds before checking again

print(f"\\nImage1 URL: {{image1_url}}")
print(f"\\nImage2 URL: {{image2_url}}")
print(f"\\nImage3 URL: {{image3_url}}")

# Check if the Batch completed successfully
if batch_status.status.lower() == "completed":
    # Retrieve the results and log
    result_file_id = batch_status.output_file_id
    results = client.files.content(result_file_id).content

    # Print response to console
    print(f"\\n🔍 AI batch response:")
    print(results)
else:
    print(f"Batch failed with status: {{batch_status.status}}")
    print(batch_status)
'''
    else:
        template = f'''# {template_description}
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
    {{
        "custom_id": "request-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {{
            "model": "{model_id}",
            "messages": [
                {{"role": "system", "content": "You are an experienced cook."}},
                {{"role": "user", "content": "What is the ultimate breakfast sandwich?"}},
            ],
            "max_completion_tokens": 1000,
        }},
    }},
    {{
        "custom_id": "request-2",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {{
            "model": "{model_id}",
            "messages": [
                {{"role": "system", "content": "You are a maths tutor."}},
                {{"role": "user", "content": "Explain the Pythagorean theorem."}},
            ],
            "max_completion_tokens": 1000,
        }},
    }},
    {{
        "custom_id": "request-3",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {{
            "model": "{model_id}",
            "messages": [
                {{
                    "role": "system",
                    "content": "You are a multilingual, experienced maths tutor.",
                }},
                {{
                    "role": "user",
                    "content": "Explain the Pythagorean theorem in Spanish",
                }},
            ],
            "max_completion_tokens": 1000,
        }},
    }},
    # Additional tasks can be added here
]

# Save tasks to a JSONL file (newline-delimited JSON)
file_name = "my_batch_request.jsonl"
with open(file_name, "w") as file:
    for request in requests:
        file.write(json.dumps(request) + "\\n")

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
    print(f"Batch status: {{batch_status.status}}")
    print(
        f"Completed tasks: {{batch_status.request_counts.completed}} / {{batch_status.request_counts.total}}"
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
    print(f"\\n🔍 AI batch response:")
    print(results)
else:
    print(f"Batch failed with status: {{batch_status.status}}")
'''
    
    return template

def get_real_time_bash_template(model: Dict[str, Any]) -> str:
    """Return a bash template for real-time API calls (to be saved as .md file)."""
    model_id = model["id"]
    model_display_name = model["display_name"]
    supports_vision = model.get("supports_vision", False)
    
    if supports_vision:
        template = f'''#!/bin/bash

# Check if API_KEY is set and not empty
if [[ -z "$API_KEY" ]]; then
    echo -e "\\nError: API_KEY environment variable is not set.\\n" >&2
fi

image_url="https://github.com/kluster-ai/klusterai-cookbook/blob/main/images/parking-image.jpeg?raw=true"

# Submit real-time request
curl https://api.kluster.ai/v1/chat/completions \\
    -H "Authorization: Bearer $API_KEY" \\
    -H "Content-Type: application/json" \\
    -d "{{
        \\"model\\": \\"{model_id}\\",
        \\"messages\\": [
            {{
                \\"role\\": \\"user\\",
                \\"content\\": [
                    {{\\"type\\": \\"text\\", \\"text\\": \\"Who can park in the area?\\"}},
                    {{\\"type\\": \\"image_url\\", \\"image_url\\": {{\\"url\\": \\"$image_url\\"}}}}
                ]
            }}
        ]
    }}"
'''
    else:
        template = f'''#!/bin/bash

# Check if API_KEY is set and not empty
if [[ -z "$API_KEY" ]]; then
    echo -e "\\nError: API_KEY environment variable is not set.\\n" >&2
fi

# Submit real-time request
curl https://api.kluster.ai/v1/chat/completions \\
    -H "Authorization: Bearer $API_KEY" \\
    -H "Content-Type: application/json" \\
    -d "{{
            \\"model\\": \\"{model_id}\\", 
            \\"messages\\": [
                {{ 
                    \\"role\\": \\"user\\", 
                    \\"content\\": \\"What is the ultimate breakfast sandwich?\\"
                }}
            ]
        }}"
'''
    
    return template

def get_batch_bash_template(model: Dict[str, Any]) -> str:
    """Return a bash template for batch API calls (to be saved as .md file)."""
    model_id = model["id"]
    model_display_name = model["display_name"]
    supports_vision = model.get("supports_vision", False)
    
    if supports_vision:
        # Using a raw string rather than f-string to avoid nested expression issues
        template = '''#!/bin/bash

# Check if API_KEY is set and not empty
if [[ -z "$API_KEY" ]]; then
    echo "Error: API_KEY environment variable is not set." >&2
fi

# Define image URLs
# Newton's cradle
image1_url="https://github.com/kluster-ai/klusterai-cookbook/blob/main/images/balls-image.jpeg?raw=true"
# Text with typos
image2_url="https://github.com/kluster-ai/klusterai-cookbook/blob/main/images/text-typo-image.jpeg?raw=true"
# Parking sign
image3_url="https://github.com/kluster-ai/klusterai-cookbook/blob/main/images/parking-image.jpeg?raw=true"

# Create request with specified structure
cat << 'EOF' > my_batch_request.template
{"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "MODEL_ID_PLACEHOLDER", "messages": [{"role": "user", "content": [{"type": "text", "text": "What is this?"}, {"type": "image_url", "image_url": {"url": "$image1_url"}}]}],"max_completion_tokens": 1000}}
{"custom_id": "request-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "MODEL_ID_PLACEHOLDER", "messages": [{"role": "user", "content": [{"type": "text", "text": "Extract the text, find typos if any."}, {"type": "image_url", "image_url": {"url": "$image2_url"}}]}],"max_completion_tokens": 1000}}
{"custom_id": "request-3", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "MODEL_ID_PLACEHOLDER", "messages": [{"role": "user", "content": [{"type": "text", "text": "Who can park in the area?"}, {"type": "image_url", "image_url": {"url": "$image3_url"}}]}],"max_completion_tokens": 1000}}
EOF

# Replace the model ID placeholder with actual model ID
sed "s/MODEL_ID_PLACEHOLDER/ACTUAL_MODEL_ID/g" my_batch_request.template > my_batch_request.jsonl

# Upload batch job file
FILE_ID=$(curl -s https://api.kluster.ai/v1/files \\
    -H "Authorization: Bearer $API_KEY" \\
    -H "Content-Type: multipart/form-data" \\
    -F "file=@my_batch_request.jsonl" \\
    -F "purpose=batch" | jq -r '.id')
echo "File uploaded, file ID: $FILE_ID"

# Submit batch job
BATCH_ID=$(curl -s https://api.kluster.ai/v1/batches \\
    -H "Authorization: Bearer $API_KEY" \\
    -H "Content-Type: application/json" \\
    -d '{
        "input_file_id": "'$FILE_ID'",
        "endpoint": "/v1/chat/completions",
        "completion_window": "24h"
    }' | jq -r '.id')
echo "Batch job submitted, job ID: $BATCH_ID"

# Poll the batch status until it's completed
STATUS="in_progress"
while [[ "$STATUS" != "completed" ]]; do
    echo "Waiting for batch job to complete... Status: $STATUS"
    sleep 10 # Wait for 10 seconds before checking again

    STATUS=$(curl -s https://api.kluster.ai/v1/batches/$BATCH_ID \\
        -H "Authorization: Bearer $API_KEY" \\
        -H "Content-Type: application/json" | jq -r '.status')
done

# Retrieve the batch output file
kluster_OUTPUT_FILE=$(curl -s https://api.kluster.ai/v1/batches/$BATCH_ID \\
    -H "Authorization: Bearer $API_KEY" \\
    -H "Content-Type: application/json" | jq -r '.output_file_id')

# Retrieve the results
OUTPUT_CONTENT=$(curl -s https://api.kluster.ai/v1/files/$kluster_OUTPUT_FILE/content \\
    -H "Authorization: Bearer $API_KEY")

# Log results
echo -e "\\nImage1 URL: $image1_url"
echo -e "\\nImage2 URL: $image2_url"
echo -e "\\nImage3 URL: $image3_url"
echo -e "\\n�� AI batch response:"
echo "$OUTPUT_CONTENT"
'''

        # Replace the placeholder with the actual model ID
        template = template.replace("ACTUAL_MODEL_ID", model_id)
    else:
        template = f'''#!/bin/bash

# Check if API_KEY is set and not empty
if [[ -z "$API_KEY" ]]; then
    echo "Error: API_KEY environment variable is not set." >&2
fi

# Create request with specified structure
cat << EOF > my_batch_request.jsonl
{{"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {{"model": "{model_id}", "messages": [{{"role": "system", "content": "You are an experienced cook."}}, {{"role": "user", "content": "What is the ultimate breakfast sandwich?"}}],"max_completion_tokens":1000}}}}
{{"custom_id": "request-2", "method": "POST", "url": "/v1/chat/completions", "body": {{"model": "{model_id}", "messages": [{{"role": "system", "content": "You are an experienced maths tutor."}}, {{"role": "user", "content": "Explain the Pythagorean theorem."}}],"max_completion_tokens":1000}}}}
{{"custom_id": "request-4", "method": "POST", "url": "/v1/chat/completions", "body": {{"model": "{model_id}", "messages":[{{"role": "system", "content": "You are a multilingual, experienced maths tutor."}}, {{"role": "user", "content": "Explain the Pythagorean theorem in Spanish"}}],"max_completion_tokens":1000}}}}
EOF

# Upload batch job file
FILE_ID=$(curl -s https://api.kluster.ai/v1/files \\
    -H "Authorization: Bearer $API_KEY" \\
    -H "Content-Type: multipart/form-data" \\
    -F "file=@my_batch_request.jsonl" \\
    -F "purpose=batch" | jq -r '.id')
echo "File uploaded, file ID: $FILE_ID"

# Submit batch job
BATCH_ID=$(curl -s https://api.kluster.ai/v1/batches \\
    -H "Authorization: Bearer $API_KEY" \\
    -H "Content-Type: application/json" \\
    -d '{{
        "input_file_id": "'$FILE_ID'",
        "endpoint": "/v1/chat/completions",
        "completion_window": "24h"
    }}' | jq -r '.id')
echo "Batch job submitted, job ID: $BATCH_ID"


# Poll the batch status until it's completed
STATUS="in_progress"
while [[ "$STATUS" != "completed" ]]; do
    echo "Waiting for batch job to complete... Status: $STATUS"
    sleep 10 # Wait for 10 seconds before checking again

    STATUS=$(curl -s https://api.kluster.ai/v1/batches/$BATCH_ID \\
        -H "Authorization: Bearer $API_KEY" \\
        -H "Content-Type: application/json" | jq -r '.status')
done

# Retrieve the batch output file
kluster_OUTPUT_FILE=$(curl -s https://api.kluster.ai/v1/batches/$BATCH_ID \\
    -H "Authorization: Bearer $API_KEY" \\
    -H "Content-Type: application/json" | jq -r '.output_file_id')

# Retrieve the results
OUTPUT_CONTENT=$(curl -s https://api.kluster.ai/v1/files/$kluster_OUTPUT_FILE/content \\
    -H "Authorization: Bearer $API_KEY")

# Log results
echo -e "\\n🔍 AI batch response:"
echo "$OUTPUT_CONTENT"
'''
    
    return template
