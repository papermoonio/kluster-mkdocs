import os
import requests
import getpass

# Prompt for API key
kluster_api_key_temp = getpass.getpass(prompt="Enter your Kluster.ai API Key: ")

# Fetch OpenAPI file with the key
if kluster_api_key_temp:
    headers = {
        "Authorization": f"Bearer {kluster_api_key_temp}"
    }
    url = "https://api.kluster.ai/v1/admin/openapi.json"
    output_filename = "kluster_openapi.json"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        
        with open(output_filename, "wb") as f:
            f.write(response.content)
        print(f"Output saved to {output_filename}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
else:
    print("API Key not entered. Request not sent.")

