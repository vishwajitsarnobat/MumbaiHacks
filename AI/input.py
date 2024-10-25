import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from functions import get_details

# Load the API key from the .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY_YEET")
with open("../templates/campaign/campaign_ai_output.json", "r") as file:
    template_json = json.load(file)
template_json_str = json.dumps(template_json, indent=4)
model_name = "gemini-1.5-flash"

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name=model_name)


# Function to fill template using Gemini API asynchronously
async def fill_template(input_json):
    for type in input_json["type"]:
        formatted_input = (
            f"You are a marketing campaign manager. The user gave the following details:\n\n"
            f"the user wants to {input_json['prompt']}\n"
            f"the user wants a campaign for this type {type}\n"
            f"the user wants to know which locations would be best to target in this region {', '.join(input_json['locations'])}\n\n"
            f"the user wants to target these languages in his campaign {', '.join(input_json['languages'])}\n\n"
            f"the user has also provided a json template which you need to fill as a json"
            f"Template: {template_json_str}\n\n"
            f"remember, Don't write anything extra not present in template and fill everything in template"
            f"Fill the fields keeping in mind the locations and languages the user, eg if target is mumbai, use keywords like in mumbai."
            f"you need to make the campaign the most successful it can be. don't give me the input I sent you again"
            f" in output. and dont format the output. replace title in explanations with the title of what youre explaining and explanation with your explanation "
            f"and replace the language with language your allocating the budget too. make it optimal, the budget being {input_json['budget_amount_micros']}"
            f"choose any one campaign_type from the given array."
        )
        # budget allocation
        response = model.generate_content(formatted_input)

        if response:  # location,age,lang,prompt
            print(response.text)
            json_str = json.loads(response.text)

            # targeting=json_str["required_inputs"]["targeting"]
            # details=get_details(targeting["locations"],targeting["age_group"],targeting["languages"],input_json['prompt'])
            # #{"language":(title,description,image)}
            # json_str["details"]=details
            return json_str
        else:
            print("Error: No response from Gemini API")
            return None


# Function to process input and return filled template
async def send_input(input_json):
    filled_template = await fill_template(input_json)
    return filled_template


# Example usage
if __name__ == "__main__":
    import asyncio

    input_json = {
        "prompt": "poster for an ad for promoting my restaurant",
        "languages": ["English", "Hindi"],
        "type": ["Ad", "Post"],
        "locations": ["Maharashtra", "ahmendabad"],
        "budget_amount_micros": 50000000,
    }

    async def main():
        result = await send_input(input_json)
        print(result)

    asyncio.run(main())
