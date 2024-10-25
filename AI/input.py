import os
import json
import httpx
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_API")


# Function to fill template using Llama API asynchronously
async def fill_template(input_json, template_json):
    url = "https://api-inference.huggingface.co/models/your-model-id"  # Replace with your model ID
    headers = {
        "Authorization": f"Bearer {LLAMA_API_KEY}",
        "Content-Type": "application/json",
    }
    formatted_input = (
        f"Fill the following template based on the requirements:\n\n"
        f"Prompt: {input_json['prompt']}\n"
        f"Languages: {', '.join(input_json['languages'])}\n"
        f"Type: {', '.join(input_json['type'])}\n"
        f"Locations: {', '.join(input_json['locations'])}\n\n"
        f"Template: {json.dumps(template_json, indent=4)}\n\n"
        f"Output the result as a JSON formatted according to the template."
    )
    payload = {"inputs": formatted_input}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None


# Function to process input and return filled template
async def send_input(input_json, template_json):
    filled_template = await fill_template(input_json, template_json)
    return filled_template


# Example usage
if __name__ == "__main__":
    import asyncio

    input_json = {
        "prompt": "poster for an ad for promoting my restaurant",
        "languages": ["English", "Hindi"],
        "type": ["Ad", "Post"],
        "locations": ["Mumbai", "Kurla"],
    }

    template_json = {
        # Example template structure
        "title": "",
        "description": "",
        "language": "",
        "type": "",
        "location": "",
    }

    async def main():
        result = await send_input(input_json, template_json)
        print(json.dumps(result, indent=4))

    asyncio.run(main())
