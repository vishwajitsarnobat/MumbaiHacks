# import requests
# import google.generativeai as genai
# import os
# import ast

# # for llama and stable fusion
# headers = {"Authorization": "Bearer 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"}

# def llama():
#     API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct" 
#     payload = {
#         "inputs": '''Here is a compelling content for an advertisement promoting Yateen's Kitchen, a popular shop selling desserts in Mumbai with a special Diwali discount:\n''',
#         "parameters": {
#             "max_new_tokens": 100,      # Maximum response length
#             "temperature": 0.7,         # Controls creativity
#             "top_p": 0.9,               # Nucleus sampling for response diversity
#             "do_sample": True           # Enables sampling for varied responses
#         }
#     }

#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()

# def image(input):
#     payload = {
#         "inputs": f'{input}'
#     }

#     response = requests.post(API_URL, headers=headers, json=payload)
#     image_data = response.content
#     # for test
#     with open("generated_image.png", "wb") as f:
#         f.write(image_data)
#     return image_data

# def gemini(prompt):
#     GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#     genai.configure(api_key=GEMINI_API_KEY)

#     model = genai.GenerativeModel(model_name="gemini-1.5-flash")

#     # Generate content with the model
#     response = model.generate_content(prompt)
#     return response.text

# # Overall workflow
# '''
# location, age, languages, prompt 
# array, string, array, string
# outputs: {"language":(title, description, image)} # this is dictionary with language as key and tuple of (title, description, image) as value
# '''
# def get_details(location, age, languages, prompt):
#     proper_prompt = '''Generate advertisement caption / content for the given prompt by the user.
#         The user requirements are given in the prompt as {prompt}.
#         The output should be based on the locations {location} targeting {age} age group, 
#         and in {languages} languages to capture cultural nuances, and regional preferences.
#         Return a dictionary with language as the key, and a tuple of title description as the value.
#         Don't return anything else (note, warning or initialisation).
#     '''

#     caption_output = gemini(proper_prompt)
#     output = ast.literal_eval(caption_output)

#     gemini_image_prompts = '''
#         Generate prompt to feed to image generator for generating advertisment. User requirements are given in prompt as {prompt}.
#         Generate seperate prompts for languages in {languages}. Make sure to capture cultural nuances, and regional preferences through the prompt.
#         Return a dictionary with language as the key, and prompt as the value.
#         Don't return anything else (note, warning or initialisation).
#     '''

#     prompts = ast.literal_eval(gemini_image_prompts)
#     images = {}
#     for language in prompts:
#         img = image(prompts[language])
#         output[language].add(img)
#     return output


import requests
import google.generativeai as genai
import os
import ast
from typing import List, Dict, Tuple, Union
from dataclasses import dataclass
from PIL import Image
import io
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AdvertisementContent:
    title: str
    description: str
    image: bytes

class AdvertisementGenerator:
    def __init__(self, hf_api_key: str, gemini_api_key: str):
        self.hf_headers = {"Authorization": f"Bearer {hf_api_key}"}
        # Keep Llama URL for future use
        self.llama_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct"
        # Stable Diffusion for image generation
        self.stable_diffusion_url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
        
        # Configure Gemini
        genai.configure(api_key=gemini_api_key)
        self.gemini_model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    def generate_multilingual_content(self, prompt: str, languages: List[str]) -> Dict[str, Tuple[str, str]]:
        """Generate multilingual content using Gemini."""
        try:
            formatted_prompt = f"""
            Create advertisement content for the following languages: {', '.join(languages)}
            Advertisement requirements: {prompt}
            
            For each language, provide a creative and culturally appropriate:
            1. Title (short and catchy)
            2. Description (compelling and detailed)
            
            Return ONLY a valid Python dictionary in this exact format, nothing else:
            {{"English": ("English Title", "English Description"), 
            "Hindi": ("Hindi Title", "Hindi Description"),
            "Marathi": ("Marathi Title", "Marathi Description")}}
            """
            
            response = self.gemini_model.generate_content(formatted_prompt)
            
            # Clean the response text
            response_text = response.text.strip()
            # Remove any markdown code block indicators if present
            response_text = response_text.replace("```python", "").replace("```", "").strip()
            
            try:
                content = ast.literal_eval(response_text)
            except Exception as parse_error:
                logger.error(f"Failed to parse response: {response_text}")
                # Fallback content creation
                content = {}
                for lang in languages:
                    content[lang] = (f"Default Title in {lang}", f"Default Description in {lang}")
            
            # Validate the response format
            for lang in languages:
                if lang not in content:
                    content[lang] = (f"Default Title in {lang}", f"Default Description in {lang}")
                if not isinstance(content[lang], tuple) or len(content[lang]) != 2:
                    content[lang] = (f"Default Title in {lang}", f"Default Description in {lang}")
                    
            return content
        except Exception as e:
            logger.error(f"Error generating multilingual content: {e}")
            # Return default content instead of raising
            return {lang: (f"Default Title in {lang}", f"Default Description in {lang}") for lang in languages}

    def generate_image_prompts(self, base_prompt: str, languages: List[str]) -> Dict[str, str]:
        """Generate culturally appropriate image prompts using Gemini."""
        try:
            prompt = f"""
            Create image generation prompts for an advertisement in different languages: {', '.join(languages)}
            Base advertisement concept: {base_prompt}
            
            Return ONLY a valid Python dictionary in this exact format, nothing else:
            {{"English": "detailed prompt for English ad",
            "Hindi": "detailed prompt for Hindi ad",
            "Marathi": "detailed prompt for Marathi ad"}}
            """
            
            response = self.gemini_model.generate_content(prompt)
            
            # Clean the response text
            response_text = response.text.strip()
            response_text = response_text.replace("```python", "").replace("```", "").strip()
            
            try:
                prompts = ast.literal_eval(response_text)
            except Exception as parse_error:
                logger.error(f"Failed to parse image prompts: {response_text}")
                # Fallback prompt creation
                prompts = {}
                for lang in languages:
                    prompts[lang] = f"Advertisement for {base_prompt} in {lang} style"
            
            # Ensure all languages have prompts
            for lang in languages:
                if lang not in prompts:
                    prompts[lang] = f"Advertisement for {base_prompt} in {lang} style"
                    
            return prompts
        except Exception as e:
            logger.error(f"Error generating image prompts: {e}")
            # Return default prompts instead of raising
            return {lang: f"Advertisement for {base_prompt} in {lang} style" for lang in languages}

    def generate_image(self, prompt: str) -> bytes:
        """Generate image using Stable Diffusion."""
        try:
            payload = {"inputs": prompt}
            response = requests.post(
                self.stable_diffusion_url, 
                headers=self.hf_headers, 
                json=payload
            )
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            raise

    def get_advertisement_details(
        self,
        locations: List[str],
        age: str,
        languages: List[str],
        prompt: str
    ) -> Dict[str, AdvertisementContent]:
        """
        Generate multilingual advertisement content including text and images.
        
        Args:
            locations: List of target locations
            age: Target age group
            languages: List of target languages
            prompt: Advertisement requirements
            
        Returns:
            Dictionary mapping languages to AdvertisementContent objects
        """
        try:
            # Enhance the base prompt with location and age information
            enhanced_prompt = f"""
            Create advertisement content for:
            - Business/Product: {prompt}
            - Target locations: {', '.join(locations)}
            - Target age group: {age}
            Make the content appealing and relevant to the specified demographic.
            """

            # Generate multilingual text content using Gemini
            text_content = self.generate_multilingual_content(enhanced_prompt, languages)

            # Generate culturally appropriate image prompts
            image_prompts = self.generate_image_prompts(enhanced_prompt, languages)

            # Generate final output
            output = {}
            for language in languages:
                try:
                    title, description = text_content[language]
                    image_data = self.generate_image(image_prompts[language])
                    output[language] = AdvertisementContent(
                        title=title,
                        description=description,
                        image=image_data
                    )
                except Exception as e:
                    logger.error(f"Error processing language {language}: {e}")
                    continue

            return output

        except Exception as e:
            logger.error(f"Error in get_advertisement_details: {e}")
            raise

    # Keep Llama function for future use
    def generate_llama_content(self, prompt: str) -> str:
        """Generate content using Llama model (kept for future use)."""
        try:
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 100,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True
                }
            }
            response = requests.post(self.llama_url, headers=self.hf_headers, json=payload)
            response.raise_for_status()
            return response.json()[0]["generated_text"]
        except Exception as e:
            logger.error(f"Error generating Llama content: {e}")
            raise

def main():
    # Example usage
    try:
        generator = AdvertisementGenerator(
            hf_api_key=os.getenv("HF_API_TOKEN"),
            gemini_api_key='AIzaSyDj97xwlHatiROdoV8B0C5BOhJhnSe85Dk'
        )

        result = generator.get_advertisement_details(
            locations=["Mumbai"],
            age="25-35",
            languages=["English", "Hindi", "Marathi"],
            prompt="Promote Yateen's Kitchen dessert shop with special Diwali discount offering traditional sweets"
        )

        # Process and save results
        for language, content in result.items():
            logger.info(f"\nLanguage: {language}")
            logger.info(f"Title: {content.title}")
            logger.info(f"Description: {content.description}")
            
            # Save image with language-specific filename
            img = Image.open(io.BytesIO(content.image))
            img.save(f"ad_image_{language.lower()}.png")
            logger.info(f"Image saved as ad_image_{language.lower()}.png")

    except Exception as e:
        logger.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()