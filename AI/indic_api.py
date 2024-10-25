import requests

# Replace with your Hugging Face API token
API_TOKEN = "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"
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# Function to translate text using Hugging Face API
def translate_text(text, src_lang="en", tgt_lang="hi"):
    # IndicTrans model hosted on Hugging Face
    model_id = "ai4bharat/IndicTrans-v2-en-indic"  # Confirm correct model name on Hugging Face Hub
    
    # Construct the payload with source and target language
    payload = {
        "inputs": f"Translate {src_lang} to {tgt_lang}: {text}"
    }
    
    # Hugging Face Inference API URL
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    
    response = requests.post(api_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        translated_text = result[0]["generated_text"]
        return translated_text
    else:
        print("Error:", response.status_code, response.text)
        return None

# Test translation
ad_text = "Discover our latest fashion collection, crafted just for you!"
translated_text = translate_text(ad_text, src_lang="en", tgt_lang="hi")
print("Hindi Translation:", translated_text)
