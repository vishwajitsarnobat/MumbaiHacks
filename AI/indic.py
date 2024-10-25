from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import gc

def setup_translator():
    # Clear memory
    torch.cuda.empty_cache()
    gc.collect()
    
    model_name = "ai4bharat/indictrans2-en-indic-1B"
    
    # Load tokenizer first
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        use_fast=False,
        trust_remote_code=True
    )
    
    # Load model with proper configuration
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        low_cpu_mem_usage=True,
        torch_dtype=torch.float32  # Use full precision for better accuracy
    )
    
    # Tie weights explicitly
    model.tie_weights()
    
    # Use CPU if GPU memory is insufficient
    device = "cpu"  # Force CPU usage for stability
    model = model.to(device)
    
    return model, tokenizer

def translate_text(text, model, tokenizer, src_lang="eng_Latn", tgt_lang="hi"):
    try:
        # Clear cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
        
        # AI4Bharat's IndicTrans2 expects specific language codes
        src_lang = "eng_Latn"  # Source is always English in Latin script
        
        # Format input text according to model's expected format
        formatted_text = f"{text} </s> {src_lang} {tgt_lang}"
        
        # Tokenize
        inputs = tokenizer(
            formatted_text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=128
        )
        
        # Move inputs to model's device
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        # Generate translation
        with torch.no_grad():
            translated_tokens = model.generate(
                **inputs,
                max_length=128,
                num_beams=4,
                length_penalty=1.0,
                early_stopping=True,
                do_sample=False
            )
        
        # Decode
        translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        
        # Cleanup
        del inputs, translated_tokens
        gc.collect()
        
        return translated_text.strip()
        
    except Exception as e:
        return f"Translation error: {str(e)}"

# Language mappings with correct codes for IndicTrans2
languages = {
    "Hindi": "hin_Deva",  # Updated language codes
    "Bengali": "ben_Beng",
    "Marathi": "mar_Deva",
    "Tamil": "tam_Taml",
    "Telugu": "tel_Telu",
    "Kannada": "kan_Knda",
    "Malayalam": "mal_Mlym",
    "Gujarati": "guj_Gujr",
    "Punjabi": "pan_Guru"
}

def main():
    print("Loading model...")
    model, tokenizer = setup_translator()
    
    # Test text
    ad_text = "Discover our latest fashion collection, crafted just for you!"
    print("\nOriginal Text:", ad_text, "\n")
    
    for language_name, lang_code in languages.items():
        print(f"Translating to {language_name}...")
        translated = translate_text(ad_text, model, tokenizer, tgt_lang=lang_code)
        print(f"{language_name} Translation: {translated}\n")
        gc.collect()

if __name__ == "__main__":
    main()