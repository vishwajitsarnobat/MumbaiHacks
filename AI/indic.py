from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Load the IndicTrans2 model and tokenizer
model_name = "ai4bharat/indictrans2-en-indic-1B"  # English to Indic languages model
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)

# Define a function to translate text
def translate_text(text, src_lang="en", tgt_lang="hi"):
    # Format the input text for translation
    formatted_text = f"Translate {src_lang} to {tgt_lang}: {text}"
    
    # Tokenize the input and generate the translation
    inputs = tokenizer(formatted_text, return_tensors="pt", padding=True)
    translated_tokens = model.generate(**inputs)
    
    # Decode the translated tokens to text
    translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    return translated_text

# Sample text to be translated
ad_text = "Discover our latest fashion collection, crafted just for you!"

# Translate into different Indian languages
languages = {
    "Hindi": "hi",
    "Bengali": "bn",
    "Marathi": "mr",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Gujarati": "gu",
    "Punjabi": "pa"
}

# Perform translations
for language_name, lang_code in languages.items():
    translated_text = translate_text(ad_text, src_lang="en", tgt_lang=lang_code)
    print(f"{language_name} Translation: {translated_text}")
