import google.generativeai as genai
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Prepare the input text
input_text = 'Hello, how are you today?'

# Generate content with the model
response = model.generate_content(f"Translate '{input_text}' to Hindi.")
print(response.text)