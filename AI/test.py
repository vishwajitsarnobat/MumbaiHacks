import os
from PIL import Image
import io
from functions import get_advertisement  # Import the refactored main function

def test_advertisement_generator():
    # Test parameters
    test_params = {
        "locations": ["Mumbai", "Delhi"],
        "age": "25-35",
        "languages": ["English", "Hindi", "Marathi"],
        "prompt": "Promote a new coffee shop with special breakfast combo offers"
    }

    try:
        # Generate advertisements
        results = get_advertisement(**test_params)  # Call get_advertisement directly

        # Create output directory if it doesn't exist
        os.makedirs("test_output", exist_ok=True)

        # Process and save results
        for language, content in results.items():
            print(f"\nResults for {language}:")
            print("Titles:")
            for i, title in enumerate(content.titles, 1):
                print(f"{i}. {title}")
            
            print("\nDescriptions:")
            for i, desc in enumerate(content.descriptions, 1):
                print(f"{i}. {desc}")

            # Save image
            image_path = f"test_output/ad_image_{language.lower()}.png"
            img = Image.open(io.BytesIO(content.image))
            img.save(image_path)
            print(f"Image saved to: {image_path}")

        print("\nTest completed successfully!")
        return True

    except Exception as e:
        print(f"Test failed with error: {e}")
        return False

if __name__ == "__main__":
    test_advertisement_generator()
