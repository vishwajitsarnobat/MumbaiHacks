import requests

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct"  
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()  # Assuming text output; adjust based on response

# Customize your prompt
payload = {
    "inputs": '''Here is a compelling content for an advertisement promoting Yateen's Kitchen, a popular shop selling desserts in Mumbai with a special Diwali discount:\n''',
    "parameters": {
        "max_new_tokens": 100,      # Maximum response length
        "temperature": 0.7,         # Controls creativity
        "top_p": 0.9,               # Nucleus sampling for response diversity
        "do_sample": True           # Enables sampling for varied responses
    }
}

# Send the request and print the generated text
response = query(payload)
print(response)
