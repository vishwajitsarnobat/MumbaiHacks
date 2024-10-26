import requests
import google.generativeai as genai
import ast
from typing import List, Dict, Tuple
from dataclasses import dataclass
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AdvertisementContent:
    titles: List[str]
    descriptions: List[str]
    image: bytes

# API Configuration
HF_API_KEY = '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'
GEMINI_API_KEY = 'AIzaSyDj97xwlHatiROdoV8B0C5BOhJhnSe85Dk'
HF_HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}
LLAMA_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct"
STABLE_DIFFUSION_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
GEMINI_MODEL = genai.GenerativeModel(model_name="gemini-1.5-flash")

def generate_multilingual_content(
    prompt: str, languages: List[str]
) -> Dict[str, Tuple[List[str], List[str]]]:
    """Generate multilingual content using Gemini."""
    try:
        formatted_prompt = f"""
        Create advertisement content for the following languages: {', '.join(languages)}
        Advertisement requirements: {prompt}
        
        For each language, provide:
        1. Three creative and culturally appropriate titles (short and catchy)
        2. Three compelling and detailed descriptions
        
        Return ONLY a valid Python dictionary in this exact format, nothing else:
        Dictionary with all languages in {languages} as keys, and tuple of (list_of_titles, list_of_descriptions) as values.
        Each list should contain exactly 3 items.
        """
        
        response = GEMINI_MODEL.generate_content(formatted_prompt)
        response_text = response.text.strip()
        
        try:
            content = ast.literal_eval(response_text)
        except Exception as parse_error:
            logger.error(f"Failed to parse response: {response_text}")
            content = {
                lang: (
                    [f"Default Title {i+1} in {lang}" for i in range(3)],
                    [f"Default Description {i+1} in {lang}" for i in range(3)]
                ) for lang in languages
            }
        
        return _validate_content(content, languages)
    except Exception as e:
        logger.error(f"Error generating multilingual content: {e}")
        return {
            lang: (
                [f"Default Title {i+1} in {lang}" for i in range(3)],
                [f"Default Description {i+1} in {lang}" for i in range(3)]
            ) for lang in languages
        }

def _validate_content(content: Dict, languages: List[str]) -> Dict:
    """Validate and fix content format if necessary."""
    for lang in languages:
        if lang not in content:
            content[lang] = (
                [f"Default Title {i+1} in {lang}" for i in range(3)],
                [f"Default Description {i+1} in {lang}" for i in range(3)]
            )
        if not isinstance(content[lang], tuple) or len(content[lang]) != 2:
            content[lang] = (
                [f"Default Title {i+1} in {lang}" for i in range(3)],
                [f"Default Description {i+1} in {lang}" for i in range(3)]
            )
        titles, descriptions = content[lang]
        if not isinstance(titles, list) or len(titles) != 3:
            titles = [f"Default Title {i+1} in {lang}" for i in range(3)]
        if not isinstance(descriptions, list) or len(descriptions) != 3:
            descriptions = [f"Default Description {i+1} in {lang}" for i in range(3)]
        content[lang] = (titles, descriptions)
    return content

def generate_image_prompts(base_prompt: str, languages: List[str]) -> Dict[str, str]:
    """Generate culturally appropriate image prompts using Gemini."""
    try:
        prompt = f"""
        Generate image prompts in English for advertisements tailored to different regions in India. Each region's advertisement should be described in English but incorporate cultural and regional nuances unique to that area's language and preferences.
        Base advertisement concept: {base_prompt}
        
        Return only a dictionary format where each language in {languages} is a key, and the value is the English prompt for that language's regional advertisement.
        """
        
        response = GEMINI_MODEL.generate_content(prompt)
        response_text = response.text.strip()
        
        try:
            prompts = ast.literal_eval(response_text)
        except Exception as parse_error:
            logger.error(f"Failed to parse image prompts: {parse_error}")
            prompts = {lang: f"Advertisement for {base_prompt} in {lang} style" for lang in languages}
        
        return {
            lang: prompts.get(lang, f"Advertisement for {base_prompt} in {lang} style")
            for lang in languages
        }
    except Exception as e:
        logger.error(f"Error generating image prompts: {e}")
        return {lang: f"Advertisement for {base_prompt} in {lang} style" for lang in languages}

def generate_image(prompt: str) -> bytes:
    """Generate image using Stable Diffusion."""
    try:
        payload = {"inputs": prompt}
        response = requests.post(
            STABLE_DIFFUSION_URL, headers=HF_HEADERS, json=payload
        )
        response.raise_for_status()
        return response.content
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        raise

def get_advertisement(
    locations: List[str], age: str, languages: List[str], prompt: str
) -> Dict[str, AdvertisementContent]:
    """
    Main function to generate multilingual advertisements with images.
    
    Returns:
        Dictionary mapping languages to AdvertisementContent objects
    """
    try:
        enhanced_prompt = f"""
        Create advertisement content for:
        - Business/Product: {prompt}
        - Target locations: {', '.join(locations)}
        - Target age group: {age}
        Make the content appealing and relevant to the specified demographic.
        """
        
        text_content = generate_multilingual_content(enhanced_prompt, languages)
        image_prompts = generate_image_prompts(enhanced_prompt, languages)
        
        output = {}
        for language in languages:
            try:
                titles, descriptions = text_content[language]
                image_data = generate_image(image_prompts[language])
                output[language] = AdvertisementContent(
                    titles=titles,
                    descriptions=descriptions,
                    image=image_data
                )
            except Exception as e:
                logger.error(f"Error processing language {language}: {e}")
                continue
        
        return output

    except Exception as e:
        logger.error(f"Error in get_advertisement: {e}")
        raise