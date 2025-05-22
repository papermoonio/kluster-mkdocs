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
import kluster
from typing import Dict, Any

# 1. Initialize the Kluster SDK client
# Get API key securely using getpass (will not be displayed or saved)
api_key = os.environ.get("API_KEY") or getpass.getpass("Enter your Kluster API key: ")
client = kluster.Client(api_key=api_key)

# 2. Example inputs
messages = [
    {{"role": "user", "content": "Write a poem about artificial intelligence."}}
]

# 3. Generate completion
response = client.real_time.completions.create(
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

vision_response = client.real_time.completions.create(
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
import kluster
from typing import Dict, Any

# 1. Initialize the Kluster SDK client
# Get API key securely using getpass (will not be displayed or saved)
api_key = os.environ.get("API_KEY") or getpass.getpass("Enter your Kluster API key: ")
client = kluster.Client(api_key=api_key)

# 2. Set up image URL
image_url = "https://github.com/kluster-ai/klusterai-cookbook/blob/main/images/parking-image.jpeg?raw=true"

# 3. Create input file with multiple image requests (JSONL format)
input_jsonl_path = "batch_input.jsonl"
with open(input_jsonl_path, "w") as f:
    # Example 1
    f.write(json.dumps({{
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
    }}) + "\\n")
    
    # Example 2
    f.write(json.dumps({{
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
    }}) + "\\n")

# 4. Define output file path
output_jsonl_path = "batch_output.jsonl"

# 5. Submit a batch job
batch_job = client.batch.completions.create(
    model="{model_id}",
    input_file_path=input_jsonl_path,
    output_file_path=output_jsonl_path,
)

print(f"Batch job submitted with ID: {{batch_job.id}}")

# 6. Wait for job to complete (optional)
completed_job = client.batch.jobs.wait(batch_job.id)
print(f"Batch job completed with status: {{completed_job.status}}")

# 7. Process results from output file
print("\\nBatch results:")
with open(output_jsonl_path, "r") as f:
    for i, line in enumerate(f):
        result = json.loads(line)
        print(f"\\nResult {{i+1}}:")
        print(f"Completion: {{result['choices'][0]['message']['content']}}")
        print(f"Finish reason: {{result['choices'][0]['finish_reason']}}")
        print(f"Total tokens: {{result['usage']['total_tokens']}}")
'''
    else:
        template = f'''# {template_description}
import os
import json
import getpass
import kluster
from typing import Dict, Any

# 1. Initialize the Kluster SDK client
# Get API key securely using getpass (will not be displayed or saved)
api_key = os.environ.get("API_KEY") or getpass.getpass("Enter your Kluster API key: ")
client = kluster.Client(api_key=api_key)

# 2. Create input file with multiple requests (JSONL format)
input_jsonl_path = "batch_input.jsonl"
with open(input_jsonl_path, "w") as f:
    # Example 1
    f.write(json.dumps({{
        "messages": [
            {{"role": "user", "content": "What is the capital of Argentina?"}}
        ],
        "max_tokens": 100
    }}) + "\\n")
    
    # Example 2
    f.write(json.dumps({{
        "messages": [
            {{"role": "user", "content": "Write a short poem about neural networks."}}
        ],
        "max_tokens": 150
    }}) + "\\n")
    
    # Example 3
    f.write(json.dumps({{
        "messages": [
            {{"role": "user", "content": "Create a short sci-fi story about AI in 50 words."}}
        ],
        "max_tokens": 100
    }}) + "\\n")

# 3. Define output file path
output_jsonl_path = "batch_output.jsonl"

# 4. Submit a batch job
batch_job = client.batch.completions.create(
    model="{model_id}",
    input_file_path=input_jsonl_path,
    output_file_path=output_jsonl_path,
)

print(f"Batch job submitted with ID: {{batch_job.id}}")

# 5. Wait for job to complete (optional)
completed_job = client.batch.jobs.wait(batch_job.id)
print(f"Batch job completed with status: {{completed_job.status}}")

# 6. Process results from output file
print("\\nBatch results:")
with open(output_jsonl_path, "r") as f:
    for i, line in enumerate(f):
        result = json.loads(line)
        print(f"\\nResult {{i+1}}:")
        print(f"Completion: {{result['choices'][0]['message']['content']}}")
        print(f"Finish reason: {{result['choices'][0]['finish_reason']}}")
        print(f"Total tokens: {{result['usage']['total_tokens']}}")
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
  https://api.kluster.ai/v1/real-time/completions \\
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
  https://api.kluster.ai/v1/real-time/completions \\
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
cat > batch_input.jsonl << 'EOF'
{{"messages": [{{"role": "user", "content": [{{"type": "text", "text": "Who can park in the area?"}}, {{"type": "image_url", "image_url": {{"url": "'$IMAGE_URL'"}}}}]}}], "max_tokens": 300}}
{{"messages": [{{"role": "user", "content": [{{"type": "text", "text": "What does this sign say?"}}, {{"type": "image_url", "image_url": {{"url": "'$IMAGE_URL'"}}}}]}}], "max_tokens": 300}}
EOF

# 2. Submit batch job
curl -X POST \\
  https://api.kluster.ai/v1/batch/completions \\
  -H "Authorization: Bearer $API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "model": "{model_id}",
    "input_file_url": "file://batch_input.jsonl",
    "output_file_url": "file://batch_output.jsonl"
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
cat > batch_input.jsonl << 'EOF'
{{"messages": [{{"role": "user", "content": "What is the capital of Argentina?"}}], "max_tokens": 100}}
{{"messages": [{{"role": "user", "content": "Write a short poem about neural networks."}}], "max_tokens": 150}}
{{"messages": [{{"role": "user", "content": "Create a short sci-fi story about AI in 50 words."}}], "max_tokens": 50}}
EOF

# 2. Submit batch job
curl -X POST \\
  https://api.kluster.ai/v1/batch/completions \\
  -H "Authorization: Bearer $API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "model": "{model_id}",
    "input_file_url": "file://batch_input.jsonl",
    "output_file_url": "file://batch_output.jsonl"
  }}'
'''
    
    return template
