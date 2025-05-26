"""
Template code for code snippets generation.
"""

from typing import Dict, Any

def get_real_time_template(model: Dict[str, Any]) -> str:
    """Return a Python template for real-time API calls."""
    model_id = model["id"]
    model_display_name = model["display_name"]
    template_description = f"Real-time completions with the {model_display_name} model on Kluster."
    supports_vision = model.get("supports_vision", False)
    
    # Base template for all models
    template = f'''# {template_description}
import os
import getpass
from openai import OpenAI

# 1. Initialize OpenAI client pointing to kluster.ai api
# Get API key securely using getpass (will not be displayed or saved)
api_key = os.environ.get("API_KEY") or getpass.getpass("Enter your Kluster API key: ")
client = OpenAI(
    api_key=api_key,
    base_url="https://api.kluster.ai/v1"
)

# 2. Example inputs
messages = [
    {{"role": "user", "content": "Write a poem about artificial intelligence."}}
]

# 3. Generate completion
response = client.chat.completions.create(
    model="{model_id}",
    messages=messages,
    max_tokens=100,
)

# 4. Process response
print("Model:", response.model)
print("Completion:", response.choices[0].message.content)
print("Finish reason:", response.choices[0].finish_reason)
print("Prompt tokens:", response.usage.prompt_tokens)
print("Completion tokens:", response.usage.completion_tokens)
print("Total tokens:", response.usage.total_tokens)
'''
    
    # Add vision-specific template for models that support it
    if supports_vision:
        template += f'''
# 5. Example with image input
image_url = "https://github.com/kluster-ai/klusterai-cookbook/blob/main/images/parking-image.jpeg?raw=true"

vision_messages = [
    {{
        "role": "user", 
        "content": [
            {{"type": "text", "text": "Describe what you see in this image."}},
            {{"type": "image_url", "image_url": {{"url": image_url}}}}
        ]
    }}
]

vision_response = client.chat.completions.create(
    model="{model_id}",
    messages=vision_messages,
    max_tokens=300,
)

print("\\nVision Completion:", vision_response.choices[0].message.content)
'''
    
    return template

def get_batch_template(model: Dict[str, Any]) -> str:
    """Return a Python template for batch JSONL API calls."""
    model_id = model["id"]
    model_display_name = model["display_name"]
    template_description = f"Batch completions with the {model_display_name} model on Kluster."
    supports_vision = model.get("supports_vision", False)
    
    if supports_vision:
        template = f'''# {template_description}
import os
import json
import getpass
from openai import OpenAI

# 1. Initialize OpenAI client pointing to kluster.ai api
# Get API key securely using getpass (will not be displayed or saved)
api_key = os.environ.get("API_KEY") or getpass.getpass("Enter your Kluster API key: ")
client = OpenAI(
    api_key=api_key,
    base_url="https://api.kluster.ai/v1"
)

# 2. Set up image URL
image_url = "https://github.com/kluster-ai/klusterai-cookbook/blob/main/images/parking-image.jpeg?raw=true"

# 3. Create input file with multiple image requests (JSONL format)
input_jsonl_path = "batch_input.jsonl"
with open(input_jsonl_path, "w") as f:
    # Example 1
    f.write(json.dumps({{
        "custom_id": "request-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {{
            "model": "{model_id}",
            "messages": [
                {{
                    "role": "user", 
                    "content": [
                        {{"type": "text", "text": "Who can park in the area?"}},
                        {{"type": "image_url", "image_url": {{"url": image_url}}}}
                    ]
                }}
            ],
            "max_tokens": 300
        }}
    }}) + "\\n")
    
    # Example 2
    f.write(json.dumps({{
        "custom_id": "request-2",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {{
            "model": "{model_id}",
            "messages": [
                {{
                    "role": "user", 
                    "content": [
                        {{"type": "text", "text": "What does this sign say?"}},
                        {{"type": "image_url", "image_url": {{"url": image_url}}}}
                    ]
                }}
            ],
            "max_tokens": 300
        }}
    }}) + "\\n")

# 4. Upload batch input file
with open(input_jsonl_path, "rb") as file:
    batch_input_file = client.files.create(
        file=file,
        purpose="batch"
    )

# 5. Submit batch job
batch_request = client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
)

print(f"Batch job submitted with ID: {{batch_request.id}}")

# 6. Check batch status (optional)
batch_status = client.batches.retrieve(batch_request.id)
print("Batch status: {{}}".format(batch_status.status))

# 7. When completed, retrieve and process results
# Note: In a real scenario, you would poll the status until completion
if batch_status.status == "completed":
    result_file_id = batch_status.output_file_id
    result_content = client.files.content(result_file_id)
    
    print("\\nBatch results:")
    for line in result_content.iter_lines():
        if line:
            result = json.loads(line)
            print(f"\\nRequest ID: {{result['custom_id']}}")
            if 'response' in result and 'body' in result['response']:
                response_body = result['response']['body']
                if 'choices' in response_body and len(response_body['choices']) > 0:
                    print(f"Completion: {{response_body['choices'][0]['message']['content']}}")
                    print(f"Finish reason: {{response_body['choices'][0]['finish_reason']}}")
                if 'usage' in response_body:
                    print(f"Total tokens: {{response_body['usage']['total_tokens']}}")
'''
    else:
        template = f'''# {template_description}
import os
import json
import getpass
from openai import OpenAI

# 1. Initialize OpenAI client pointing to kluster.ai api
# Get API key securely using getpass (will not be displayed or saved)
api_key = os.environ.get("API_KEY") or getpass.getpass("Enter your Kluster API key: ")
client = OpenAI(
    api_key=api_key,
    base_url="https://api.kluster.ai/v1"
)

# 2. Create input file with multiple requests (JSONL format)
input_jsonl_path = "batch_input.jsonl"
with open(input_jsonl_path, "w") as f:
    # Example 1
    f.write(json.dumps({{
        "custom_id": "request-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {{
            "model": "{model_id}",
            "messages": [
                {{"role": "user", "content": "What is the capital of Argentina?"}}
            ],
            "max_tokens": 100
        }}
    }}) + "\\n")
    
    # Example 2
    f.write(json.dumps({{
        "custom_id": "request-2",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {{
            "model": "{model_id}",
            "messages": [
                {{"role": "user", "content": "Write a short poem about neural networks."}}
            ],
            "max_tokens": 150
        }}
    }}) + "\\n")
    
    # Example 3
    f.write(json.dumps({{
        "custom_id": "request-3",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {{
            "model": "{model_id}",
            "messages": [
                {{"role": "user", "content": "Create a short sci-fi story about AI in 50 words."}}
            ],
            "max_tokens": 100
        }}
    }}) + "\\n")

# 3. Upload batch input file
with open(input_jsonl_path, "rb") as file:
    batch_input_file = client.files.create(
        file=file,
        purpose="batch"
    )

# 4. Submit batch job
batch_request = client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
)

print(f"Batch job submitted with ID: {{batch_request.id}}")

# 5. Check batch status (optional)
batch_status = client.batches.retrieve(batch_request.id)
print("Batch status: {{}}".format(batch_status.status))

# 6. When completed, retrieve and process results
# Note: In a real scenario, you would poll the status until completion
if batch_status.status == "completed":
    result_file_id = batch_status.output_file_id
    result_content = client.files.content(result_file_id)
    
    print("\\nBatch results:")
    for line in result_content.iter_lines():
        if line:
            result = json.loads(line)
            print(f"\\nRequest ID: {{result['custom_id']}}")
            if 'response' in result and 'body' in result['response']:
                response_body = result['response']['body']
                if 'choices' in response_body and len(response_body['choices']) > 0:
                    print(f"Completion: {{response_body['choices'][0]['message']['content']}}")
                    print(f"Finish reason: {{response_body['choices'][0]['finish_reason']}}")
                if 'usage' in response_body:
                    print(f"Total tokens: {{response_body['usage']['total_tokens']}}")
'''
    
    return template

def get_real_time_bash_template(model: Dict[str, Any]) -> str:
    """Return a bash template for real-time API calls (to be saved as .md file)."""
    model_id = model["id"]
    model_display_name = model["display_name"]
    supports_vision = model.get("supports_vision", False)
    
    if supports_vision:
        template = f'''# Real-time API completions with {model_display_name} model (vision-capable)

# Ensure your API key is set in your environment
# export API_KEY="your_api_key_here"

# Check if API_KEY is set and not empty
if [[ -z "$API_KEY" ]]; then
    echo -e "\nError: API_KEY environment variable is not set.\n" >&2
fi

# Define image URL 
IMAGE_URL="https://github.com/kluster-ai/klusterai-cookbook/blob/main/images/parking-image.jpeg?raw=true"

curl -X POST \\
  https://api.kluster.ai/v1/chat/completions \\
  -H "Authorization: Bearer $API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "model": "{model_id}",
    "messages": [
      {{
        "role": "user", 
        "content": [
          {{ "type": "text", "text": "Describe what you see in this image." }},
          {{ "type": "image_url", "image_url": {{ "url": "'$IMAGE_URL'" }} }}
        ]
      }}
    ],
    "max_tokens": 300
  }}'
'''
    else:
        template = f'''# Real-time API completions with {model_display_name} model

# Ensure your API key is set in your environment
# export API_KEY="your_api_key_here"

curl -X POST \\
  https://api.kluster.ai/v1/chat/completions \\
  -H "Authorization: Bearer $API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "model": "{model_id}",
    "messages": [
      {{
        "role": "user", 
        "content": "Write a poem about artificial intelligence."
      }}
    ],
    "max_tokens": 100
  }}'
'''
    
    return template

def get_batch_bash_template(model: Dict[str, Any]) -> str:
    """Return a bash template for batch API calls (to be saved as .md file)."""
    model_id = model["id"]
    model_display_name = model["display_name"]
    supports_vision = model.get("supports_vision", False)
    
    if supports_vision:
        template = f'''# Batch API completions with {model_display_name} model (vision-capable)

# Ensure your API key is set in your environment
# export API_KEY="your_api_key_here"

# Check if API_KEY is set and not empty
if [[ -z "$API_KEY" ]]; then
    echo -e "\nError: API_KEY environment variable is not set.\n" >&2
fi

# Define image URL
IMAGE_URL="https://github.com/kluster-ai/klusterai-cookbook/blob/main/images/parking-image.jpeg?raw=true"

# 1. Create input file (batch_input.jsonl) with image content
cat > batch_input.jsonl << EOF
{{"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {{"model": "{model_id}", "messages": [{{"role": "user", "content": [{{"type": "text", "text": "Who can park in the area?"}}, {{"type": "image_url", "image_url": {{"url": "$IMAGE_URL"}}}}]}}], "max_tokens": 300}}}}
{{"custom_id": "request-2", "method": "POST", "url": "/v1/chat/completions", "body": {{"model": "{model_id}", "messages": [{{"role": "user", "content": [{{"type": "text", "text": "What does this sign say?"}}, {{"type": "image_url", "image_url": {{"url": "$IMAGE_URL"}}}}]}}], "max_tokens": 300}}}}
EOF

# 2. Upload batch input file
UPLOAD_RESPONSE=$(curl -X POST \\
  https://api.kluster.ai/v1/files \\
  -H "Authorization: Bearer $API_KEY" \\
  -F "purpose=batch" \\
  -F "file=@batch_input.jsonl")

# Extract file ID from upload response
FILE_ID=$(echo $UPLOAD_RESPONSE | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)

# 3. Submit batch job
curl -X POST \\
  https://api.kluster.ai/v1/batches \\
  -H "Authorization: Bearer $API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "input_file_id": "'$FILE_ID'",
    "endpoint": "/v1/chat/completions",
    "completion_window": "24h"
  }}'
'''
    else:
        template = f'''# Batch API completions with {model_display_name} model

# Ensure your API key is set in your environment
# export API_KEY="your_api_key_here"

# Check if API_KEY is set and not empty
if [[ -z "$API_KEY" ]]; then
    echo -e "\nError: API_KEY environment variable is not set.\n" >&2
fi

# 1. Create input file (batch_input.jsonl)
cat > batch_input.jsonl << EOF
{{"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {{"model": "{model_id}", "messages": [{{"role": "user", "content": "What is the capital of Argentina?"}}], "max_tokens": 100}}}}
{{"custom_id": "request-2", "method": "POST", "url": "/v1/chat/completions", "body": {{"model": "{model_id}", "messages": [{{"role": "user", "content": "Write a short poem about neural networks."}}], "max_tokens": 150}}}}
{{"custom_id": "request-3", "method": "POST", "url": "/v1/chat/completions", "body": {{"model": "{model_id}", "messages": [{{"role": "user", "content": "Create a short sci-fi story about AI in 50 words."}}], "max_tokens": 100}}}}
EOF

# 2. Upload batch input file
UPLOAD_RESPONSE=$(curl -X POST \\
  https://api.kluster.ai/v1/files \\
  -H "Authorization: Bearer $API_KEY" \\
  -F "purpose=batch" \\
  -F "file=@batch_input.jsonl")

# Extract file ID from upload response
FILE_ID=$(echo $UPLOAD_RESPONSE | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)

# 3. Submit batch job
curl -X POST \\
  https://api.kluster.ai/v1/batches \\
  -H "Authorization: Bearer $API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "input_file_id": "'$FILE_ID'",
    "endpoint": "/v1/chat/completions",
    "completion_window": "24h"
  }}'
'''
    
    return template
