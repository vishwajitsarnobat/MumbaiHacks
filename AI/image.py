import requests

API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

payload = {
    "inputs": '''You are a digital marketing firm. Your client wants a advertisemnt image to post on instagram.
    Your client owns a sweets shop in Mumbai selling famous sweets in Mumbai. He wants the advertisement for boosting sales in Diwali.
    Include diwali sale offer which gives 20 percent off on any sweets'''
}

# Send the request
image_data = query(payload)

# Save the image to a file
with open("generated_image.png", "wb") as f:
    f.write(image_data)

print("Image generated and saved as generated_image.png")