import requests
import google.generativeai as genai
import os
import ast
from typing import List, Dict, Tuple, Union
from dataclasses import dataclass
from PIL import Image
import io
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AdvertisementContent:
    titles: List[str]
    descriptions: List[str]
    image: bytes

    def to_dict(self) -> Dict:
        """Convert AdvertisementContent to dictionary format"""
        return {
            'titles': self.titles,
            'descriptions': self.descriptions,
            'image': self.image.hex() if self.image else None  # Convert bytes to hex string for JSON serialization
        }

class AdvertisementGenerator:
    def __init__(self, hf_api_key: str = None, gemini_api_key: str = None):
        # Use environment variables if keys are not provided
        self.hf_api_key = hf_api_key or os.getenv('HUGGINGFACE_API_KEY')
        self.gemini_api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.hf_api_key or not self.gemini_api_key:
            raise ValueError("API keys must be provided either through parameters or environment variables")
            
        self.hf_headers = {"Authorization": f"Bearer {self.hf_api_key}"}
        self.llama_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct"
        self.stable_diffusion_url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
        
        # Configure Gemini
        genai.configure(api_key=self.gemini_api_key)
        self.gemini_model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    def generate_multilingual_content(
        self, prompt: str, languages: List[str]
    ) -> Dict[str, Tuple[str, str]]:
        """Generate multilingual content using Gemini."""
        try:
            formatted_prompt = f"""
            Create advertisement content for the following languages: {', '.join(languages)}
            Advertisement requirements: {prompt}
            
            For each language, provide 3 creative and culturally appropriate:
            1. Title (short and catchy)
            2. Description (compelling and detailed)
            
            Return ONLY a valid Python dictionary in this exact format, nothing else:
            Dictionary with all languages in {languages} as the keys, and tuple of (title, description) as the value.
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

    def generate_image_prompts(
        self, base_prompt: str, languages: List[str]
        ) -> Dict[str, str]:
        """Generate culturally appropriate image prompts using Gemini."""
        try:
            prompt = f"""
            Generate image prompts in English for advertisements tailored to different regions in India. Each region's advertisement should be described in English but incorporate cultural and regional nuances unique to that area's language and preferences, so the images feel localized and authentic. 
            Base advertisement concept: {base_prompt}
            
            Return only a dictionary format where each language in {languages} is a key, and the value is the English prompt for that language's regional advertisement. Each prompt should emphasize the cultural elements, holiday traditions, colors, foods, or attire familiar to that language region while aligning with the base advertisement concept.
            """

            response = self.gemini_model.generate_content(prompt)
            
            # Clean and check response text
            response_text = response.text.strip()
            print(f"Raw image prompt response: {response_text}")  # For debugging

            # Remove any triple backticks and language specifier
            if response_text.startswith("```") and response_text.endswith("```"):
                response_text = response_text[3:-3].strip()
            response_text = response_text.replace("json", "").strip()  # Remove "json" if present

            try:
                # Use ast.literal_eval to safely evaluate the cleaned string as a dictionary
                prompts = ast.literal_eval(response_text)
            except Exception as parse_error:
                logger.error(f"Failed to parse image prompts with ast.literal_eval: {parse_error}")
                # Fallback: Generate a default dictionary if parsing fails
                prompts = {lang: f"Advertisement for {base_prompt} in {lang} style" for lang in languages}

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
                self.stable_diffusion_url, headers=self.hf_headers, json=payload
            )
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            raise

    def generate_advertisements(
        locations: List[str],
        age: str,
        languages: List[str],
        prompt: str,
        hf_api_key: str = None,
        gemini_api_key: str = None,
        save_images: bool = False,
        output_dir: str = None
    ) -> Dict[str, Dict]:
        """
        Generate advertisements based on given parameters.
        
        Args:
            locations (List[str]): List of target locations
            age (str): Target age group
            languages (List[str]): List of target languages
            prompt (str): Advertisement requirements
            hf_api_key (str, optional): HuggingFace API key
            gemini_api_key (str, optional): Gemini API key
            save_images (bool, optional): Whether to save generated images to disk
            output_dir (str, optional): Directory to save images if save_images is True
        
        Returns:
            Dict[str, Dict]: Dictionary with language keys and advertisement content values
        """
        try:
            # Initialize the generator
            generator = AdvertisementGenerator(
                hf_api_key=hf_api_key,
                gemini_api_key=gemini_api_key
            )

            # Generate the advertisements
            result = generator.get_advertisement_details(
                locations=locations,
                age=age,
                languages=languages,
                prompt=prompt
            )

            # Convert results to dictionary format
            output = {}
            for language, content in result.items():
                # Convert AdvertisementContent to dictionary
                output[language] = content.to_dict()
                
                # Optionally save images
                if save_images:
                    if output_dir:
                        os.makedirs(output_dir, exist_ok=True)
                        image_path = os.path.join(output_dir, f"ad_image_{language.lower()}.png")
                    else:
                        image_path = f"ad_image_{language.lower()}.png"
                    
                    img = Image.open(io.BytesIO(content.image))
                    img.save(image_path)
                    logger.info(f"Image saved as {image_path}")

            return output

        except Exception as e:
            logger.error(f"Error generating advertisements: {e}")
            raise

# Example usage
if __name__ == "__main__":
    try:
        # This is just for testing the module directly
        result = generate_advertisements(
            locations=["Mumbai"],
            age="25-35",
            languages=["English", "Hindi", "Marathi"],
            prompt="Promote Yateen's Kitchen dessert shop with special Diwali discount offering traditional sweets",
            save_images=True
        )
        
        # Print results
        for language, content in result.items():
            print(f"\nLanguage: {language}")
            for i in range(3):
                print(f"Title {i+1}: {content['titles'][i]}")
                print(f"Description {i+1}: {content['descriptions'][i]}")
            print(f"Image data length: {len(content['image']) if content['image'] else 'No image'}")
            
    except Exception as e:
        logger.error(f"Error in main: {e}")
