import requests
import google.generativeai as genai
import os

# for llama and stable fusion
headers = {"Authorization": "Bearer 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"}

def llama():
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct" 
    payload = {
        "inputs": '''Here is a compelling content for an advertisement promoting Yateen's Kitchen, a popular shop selling desserts in Mumbai with a special Diwali discount:\n''',
        "parameters": {
            "max_new_tokens": 100,      # Maximum response length
            "temperature": 0.7,         # Controls creativity
            "top_p": 0.9,               # Nucleus sampling for response diversity
            "do_sample": True           # Enables sampling for varied responses
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def image():
    payload = {
        "inputs": '''You are a digital marketing firm. Your client wants a advertisemnt image to post on instagram.
        Your client owns a sweets shop in Mumbai selling famous sweets in Mumbai. He wants the advertisement for boosting sales in Diwali.
        Include diwali sale offer which gives 20 percent off on any sweets'''
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    image_data = response.content
    # for test
    with open("generated_image.png", "wb") as f:
        f.write(image_data)
    return image_data

def gemini():
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # Prepare the input text
    input_text = 'Hello, how are you today?'

    # Generate content with the model
    response = model.generate_content(f"Translate '{input_text}' to Hindi.")
    return response.text

# Overall workflow
