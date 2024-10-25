import requests

# Define the API endpoint and add your Hugging Face API token
API_URL = "https://api-inference.huggingface.co/models/ai4bharat/indictrans2-en-indic-1B"  # Example for English to Hindi
headers = {"Authorization": "Bearer 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"}

# Define the function to send a query to the IndicTrans model
def translate_text(text, target_language="hi"):
    # Update API URL based on target language if different models exist per language
    # For multi-language support, you may use a combined model, if available, or route to different endpoints
    
    payload = {
        "inputs": '''Indulge in Delicious Desserts this Diwali with Yateen's Kitchen!\n\n
        Get Ready to Treat Your Taste Buds with our Wide Range of Mouth-Watering Desserts at Unbeatable Prices!'''
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Example text to translate
text_to_translate = "Welcome to Yateen's Kitchen! We are offering special discounts on desserts this Diwali."
target_language = "hi"  # Set to your desired language code

# Translate and display the result
translated_response = translate_text(text_to_translate, target_language)
print(translated_response)