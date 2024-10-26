import requests
import google.generativeai as genai
import os
import ast

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

def image(input):
    payload = {
        "inputs": f'{input}'
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    image_data = response.content
    # for test
    with open("generated_image.png", "wb") as f:
        f.write(image_data)
    return image_data

def gemini(prompt):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # Generate content with the model
    response = model.generate_content(prompt)
    return response.text

# Overall workflow
'''
location, age, languages, prompt
array, string, array, string
outputs: {"language":(title, description, image)} # this is dictionary with language as key and tuple of (title, description, image) as value
'''
def get_details(location, age, languages, prompt):
    proper_prompt = '''Generate advertisement caption / content for the given prompt by the user.
        The user requirements are given in the prompt as {prompt}.
        The output should be based on the locations {location} targeting {age} age group,
        and in {languages} languages to capture cultural nuances, and regional preferences.
        Return a dictionary with language as the key, and a tuple of title description as the value.
        Don't return anything else (note, warning or initialisation).
    '''

    caption_output = gemini(proper_prompt)
    output = ast.literal_eval(caption_output)

    gemini_image_prompts = '''
        Generate prompt to feed to image generator for generating advertisment. User requirements are given in prompt as {prompt}.
        Generate seperate prompts for languages in {languages}. Make sure to capture cultural nuances, and regional preferences through the prompt.
        Return a dictionary with language as the key, and prompt as the value.
        Don't return anything else (note, warning or initialisation).
    '''

    prompts = ast.literal_eval(gemini_image_prompts)
    images = {}
    for language in prompts:
        img = image(prompts[language])
        output[language].add(img)
    return output