import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from functions import generate_ad_content
from datetime import datetime

# Load the API key from the .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY_YEET")
with open("../templates/campaign_ai_output.json", "r") as file:
    template_json = json.load(file)
template_json_str = json.dumps(template_json, indent=4)
model_name = "gemini-1.5-flash"

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name=model_name)


# Function to fill template using Gemini API asynchronously
async def fill_template(input_json):
    start_date = datetime.today().strftime("%Y-%m-%d")
    output_json = {}

    formatted_input = (
        f"You are a marketing campaign manager. The user gave the following details:\n\n"
        f"the user wants to {input_json['prompt']}\n"
        f"the user wants to know which locations would be best to target in this region {', '.join(input_json['locations'])}\n\n"
        f"the user wants to target these languages in his campaign {', '.join(input_json['languages'])}\n\n"
        f"the user has also provided a json template which you need to fill as a json."
        f"Template: {template_json_str}\n\n"
        f" you can only use one language per campaign. and set start date as {start_date}."
        f"remember, Don't write anything extra not present in template and fill everything in template and don't give me the input I sent you again in output"
        f"Fill the fields keeping in mind the locations and languages the user, eg if target is mumbai, use keywords like in mumbai."
        f"you need to make the campaign the most successful it can be."
        f"allocate the budget optimal across all campaigns, the budget being {input_json['budget_amount_micros']}"
        f"format the summary as json. it should have details like why were the decisions made, what benefits they will have and must have a itemized list of language in campaign,campaign name and budget alloted"
    )
    # budget allocation

    response = model.generate_content(formatted_input)

    if response:  # location,age,lang,prompt
        print(response.text)
        json_str = json.loads(response.text)
        for i in range(len(json_str["campaigns"])):
            json_str["campaigns"][i]["campaign"]["status"] = "ENABLED"
            json_str["campaigns"][i]["campaign"]["manual_cpc"] = True
            json_str["campaigns"][i]["campaign"]["delivery_method"] = "STANDARD"
            json_str["campaigns"][i]["campaign"]["conversion_goals"] = "Account-default"
            json_str["campaigns"][i]["campaign"]["marketing_objective"] = None
            json_str["campaigns"][i]["campaign"]["start_date"] = start_date

            json_str["campaigns"][i]["ad_group"]["status"] = "ENABLED"

            json_str["campaigns"][i]["ad"]["final_url"] = "https://eg.com"
            json_str["campaigns"][i]["ad"]["path1"] = ""
            json_str["campaigns"][i]["ad"]["path2"] = ""
            json_str["campaigns"][i]["ad"]["customizer_attribute_name"] = None

        targeting = json_str["campaign_data"]
        (status, details) = generate_ad_content(
            targeting["locations"],
            "general public",
            input_json["languages"],
            input_json["prompt"],
        )
        # {"language":([title],[description],image)}
        if status:
            for language in details:
                input_json["campaigns"]["ad"]["headlines"] = []
                input_json["campaigns"]["ad"]["descriptions"][i] = []
                input_json["campaigns"]["ad"]["images"][0] = details[language][2]
                for i in len(details[language][0]):
                    input_json["campaigns"]["ad"]["headlines"].push(
                        details[language][0][i]
                    )
                    input_json["campaigns"]["ad"]["descriptions"][i].push(
                        details[language][1][i]
                    )
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
        "languages": ["English"],
        "type": ["Ad", "Post"],
        "locations": ["Maharashtra", "ahmendabad"],
        "budget_amount_micros": 500000,
    }

    async def main():
        result = await send_input(input_json)
        print(result)

    asyncio.run(main())
