import logging
from typing import List, Dict, Union
import io
import base64
from PIL import Image
import aiohttp
import google.generativeai as genai
import ast
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_multilingual_content(
    gemini_model: genai.GenerativeModel,
    prompt: str, 
    languages: List[str]
) -> Dict[str, tuple[str, str]]:
    """Generate multilingual content using Gemini."""
    try:
        formatted_prompt = f"""
        Create advertisement content for the following languages: {', '.join(languages)}
        Advertisement requirements: {prompt}
        
        For each language, provide a creative and culturally appropriate:
        1. Title (short and catchy)
        2. Description (compelling and detailed)
        
        Return ONLY a valid Python dictionary in this exact format, nothing else:
        Dictionary with all languages in {languages} as keys, and tuple of (title, description) as value.
        """

        response = await gemini_model.generate_content(formatted_prompt)
        
        # Clean the response text
        response_text = response.text.strip()
        response_text = response_text.replace("```python", "").replace("```", "").strip()
        
        try:
            content = ast.literal_eval(response_text)
        except Exception as parse_error:
            logger.error(f"Failed to parse response: {response_text}")
            content = {lang: (f"Title in {lang}", f"Description in {lang}") for lang in languages}
        
        return content

    except Exception as e:
        logger.error(f"Error generating multilingual content: {e}")
        return {lang: (f"Title in {lang}", f"Description in {lang}") for lang in languages}

async def generate_image_prompts(
    gemini_model: genai.GenerativeModel,
    base_prompt: str, 
    languages: List[str]
) -> Dict[str, str]:
    """Generate culturally appropriate image prompts."""
    try:
        prompt = f"""
        Generate image prompts in English for advertisements tailored to different regions.
        Base advertisement concept: {base_prompt}
        
        Return only a dictionary with {languages} as keys and English prompts as values.
        Make each prompt culturally relevant to the language region.
        """

        response = await gemini_model.generate_content(prompt)
        response_text = response.text.strip().replace("```", "").strip()
        
        try:
            prompts = ast.literal_eval(response_text)
        except Exception:
            prompts = {lang: f"Advertisement for {base_prompt} in {lang} style" for lang in languages}
            
        return prompts

    except Exception as e:
        logger.error(f"Error generating image prompts: {e}")
        return {lang: f"Advertisement for {base_prompt} in {lang} style" for lang in languages}

async def generate_image(
    session: aiohttp.ClientSession,
    stable_diffusion_url: str,
    hf_headers: Dict[str, str],
    prompt: str
) -> bytes:
    """Generate image using Stable Diffusion."""
    try:
        async with session.post(
            stable_diffusion_url,
            headers=hf_headers,
            json={"inputs": prompt}
        ) as response:
            response.raise_for_status()
            return await response.read()
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        raise

def convert_image_to_base64(image_bytes: bytes) -> str:
    """Convert image bytes to base64 string."""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        logger.error(f"Error converting image to base64: {e}")
        raise

async def generate_ad_content(
    location: Union[str, List[str]],
    age_group: str,
    languages: List[str],
    prompt: str
) -> Dict[str, Union[bool, Dict, str]]:
    """
    Generate multilingual advertisement content including text and images.
    Returns dictionary with success status and either data or error message.
    """
    try:
        # Initialize API configurations
        hf_headers = {"Authorization": f"Bearer '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'"}
        stable_diffusion_url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
        
        # Configure Gemini
        gemini_api_key = 'AIzaSyDj97xwlHatiROdoV8B0C5BOhJhnSe85Dk'
        genai.configure(api_key=gemini_api_key)
        gemini_model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        # Normalize location to list
        locations = [location] if isinstance(location, str) else location
        
        # Enhanced prompt
        enhanced_prompt = f"""
        Create advertisement content for:
        - Business/Product: {prompt}
        - Target locations: {', '.join(locations)}
        - Target age group: {age_group}
        Make the content appealing and relevant to the specified demographic.
        """

        # Generate text content and image prompts concurrently
        text_content = await generate_multilingual_content(gemini_model, enhanced_prompt, languages)
        image_prompts = await generate_image_prompts(gemini_model, enhanced_prompt, languages)

        # Generate images
        result = {}
        async with aiohttp.ClientSession() as session:
            for lang in languages:
                try:
                    # Generate image
                    image_bytes = await generate_image(
                        session,
                        stable_diffusion_url,
                        hf_headers,
                        image_prompts[lang]
                    )
                    
                    # Convert image to base64
                    image_base64 = convert_image_to_base64(image_bytes)
                    
                    # Get title and description
                    title, description = text_content[lang]
                    
                    # Store results
                    result[lang] = {
                        "title": title,
                        "description": description,
                        "image": f"data:image/png;base64,{image_base64}"
                    }
                except Exception as e:
                    logger.error(f"Error processing language {lang}: {e}")
                    continue

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        error_msg = f"Error generating advertisement content: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }